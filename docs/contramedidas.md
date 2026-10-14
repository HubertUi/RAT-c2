# Contramedidas y Remediación

## 1. Detección de Sandbox/Anti-Análisis

### Técnicas de Detección
1. **Monitoreo de Procesos**
   - Detectar herramientas de análisis: wireshark.exe, procmon.exe, processhacker.exe
   - Monitorear debuggers: idaq.exe, x32dbg.exe, x64dbg.exe, ollydbg.exe
   - Verificar patrones de actividad sospechosa

2. **Recursos del Sistema**
   - Verificar RAM disponible (< 2GB indica sandbox)
   - Revisar número de cores (< 2 indica VM)
   - Analizar uptime (ejecuciones rápidas indican análisis)
   - Detectar actividad de mouse (inusual en sandboxes)

3. **Nombres y Configuración**
   - Verificar nombres de usuario: sandbox, virus, malware, test, admin
   - Revisar nombres de host: sandbox, cuckoo, virus, malware, sample
   - Monitorear variables de entorno sospechosas

### Reglas de Detección YARA
```yaml
rule sandbox_detection:
  meta:
    description: Detecta sandboxes comunes
    author: Security Research
  strings:
    $sandbox_user = /sandbox|virus|malware|test/user
    $analysis_tool = /wireshark|procmon|processhacker|autoruns/ 
    $low_memory = { 08 00 00 00 00 00 00 00 01 00 00 00 }
  condition:
    any of ($sandbox_user, $analysis_tool) or $low_memory
```

## 2. Detección de Persistencia

### Técnicas de Detección
1. **Registry Autostart**
   ```powershell
   Get-ItemProperty HKCU:\Software\Microsoft\Windows\CurrentVersion\Run
   Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Run
   ```

2. **Tareas Programadas**
   ```powershell
   Get-ScheduledTask | Where-Object {$_.Actions.Execute -like "*update*"}
   ```

3. **Startup Folder**
   - Revisar `shell:startup` y `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`
   - Detectar accesos directos sospechosos

4. **WMI Event Consumers**
   ```powershell
   Get-WmiObject -Namespace "root\subscription" -Class __EventFilter
   Get-WmiObject -Namespace "root\subscription" -Class CommandLineEventConsumer
   ```

### Scripts de Detección
```powershell
# Detección completa de persistencia
function Detect-Persistence {
    Write-Host "=== Detección de Persistencia ==="
    
    # 1. Registry
    Write-Host "[+] Verificando Registro..."
    $runKeys = @(
        "HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
        "HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    )
    
    foreach ($key in $runKeys) {
        try {
            $values = Get-ItemProperty $key
            foreach ($value in $values.PSObject.Properties) {
                if ($value.Name -like "*update*") {
                    Write-Host "  ENCONTRADO: $key\$($value.Name) = $($value.Value)"
                }
            }
        } catch {
            Write-Host "  Error accediendo $key"
        }
    }
    
    # 2. Tareas programadas
    Write-Host "[+] Verificando Tareas Programadas..."
    $suspiciousTasks = Get-ScheduledTask | Where-Object {
        $_.Actions.Execute -like "*.exe" -and 
        ($_.Actions.Execute -like "*update*" -or $_.Actions.Execute -like "*windows*" -or $_.Actions.Execute -like "*microsoft*" )
    }
    
    if ($suspiciousTasks) {
        foreach ($task in $suspiciousTasks) {
            Write-Host "  ENCONTRADO: $($task.TaskName) - $($task.Actions.Execute)"
        }
    }
    
    # 3. Suscripciones WMI
    Write-Host "[+] Verificando Suscripciones WMI..."
    try {
        $wmiFilters = Get-WmiObject -Namespace "root\subscription" -Class __EventFilter
        foreach ($filter in $wmiFilters) {
            if ($filter.Name -like "*update*") {
                Write-Host "  ENCONTRADO: Filter WMI $($filter.Name)"
            }
        }
    } catch {
        Write-Host "  No se pudieron acceder suscripciones WMI"
    }
}
```

## 3. Detección de Recopilación de Inteligencia

### Técnicas de Detección
1. **Exfiltricación de Datos**
   - Monitorear conexiones salientes a dominios sospechosos
   - Detectar actividad de envío de archivos inusual
   - Revisar tráfico de red para payloads grandes

2. **Reconocimiento de Red**
   ```powershell
   # Detectar escaneos de red
   Get-WinEvent -LogName Microsoft-Windows-Security-Auditing | 
   Where-Object {$_.Message -like "*Port*"} | 
   Select-Object TimeCreated, Message
   ```

3. **InfoSec del Sistema**
   - Revisar registry para ubicaciones sospechosas
   - Detectar aplicaciones ocultas o no autorizadas
   - Monitorear procesos inusuales

## 4. Detección de C2 vía Discord

### Técnicas de Detección
1. **Análisis de Red**
   - Monitorear tráfico HTTPS a endpoints de Discord
   - Detectar procesos inusuales haciendo conexiones salientes
   - Revisar certificados SSL para dominios desconocidos

2. **Monitor de Procesos**
   ```powershell
   # Detectar procesos Discord
   Get-Process | Where-Object {
       $_.MainWindowTitle -like "*Discord*" -or 
       $_.Description -like "*Discord*"
   } | Select-Object ProcessName, Id, CPU, WorkingSet
   ```

3. **Análisis de Tráfico**
   ```bash
   # Utilizar tcpdump para capturar tráfico Discord
   sudo tcpdump -i any -w discord_traffic.pcap 'tcp port 443'
   ```

### Scripts de Detección
```python
# Script de detección de C2 basado en Discord
def detect_discord_c2():
    import subprocess
    import json
    
    # Obtener lista de procesos
    processes = subprocess.run(
        ['tasklist'], 
        capture_output=True, 
        text=True
    ).stdout
    
    # Buscar procesos Discord sospechosos
    suspicious_processes = []
    for line in processes.split('\n'):
        if 'discord' in line.lower() and not 'chrome' in line.lower():
            suspicious_processes.append(line)
    
    if suspicious_processes:
        print("⚠️  Procesos Discord sospechosos detectados:")
        for proc in suspicious_processes:
            print(f"  - {proc}")
    
    return suspicious_processes
```

## 5. Detección de Capacidades del RAT

### Técnicas de Detección
1. **Permisos Elevados**
   - Detectar procesos con privilegios de SYSTEM/administrador
   - Monitorear intentos de elevación

2. **Actividad Inusual**
   - Detectar ejecuciones de procesos sospechosos
   - Monitorear manipulación de archivos
   - Revisar actividad de registro

3. **Comandos Sospechosos**
   ```powershell
   # Detectar patrones de comandos sospechosos
   Get-WinEvent -LogName PowerShell-Core/Operational | 
   Where-Object {
       $_.Message -like "*shell*" -or 
       $_.Message -like "*screenshot*" -or
       $_.Message -like "*download*"
   } | Select-Object TimeCreated, Message
   ```

## 6. Guías de Remediación

### 1. Eliminación de Persistencia
```powershell
# Eliminar claves de registry
Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "WindowsUpdate" -ErrorAction SilentlyContinue

# Eliminar tareas programadas
Unregister-ScheduledTask -TaskName "WindowsUpdateTask" -Confirm:$false

# Eliminar suscripciones WMI
$filter = Get-WmiObject -Namespace "root\subscription" -Class __EventFilter | Where-Object {$_.Name -like "*update*"}
if ($filter) {
    Remove-WmiObject -InputObject $filter
}
```

### 2. Limpieza de Archivos
```powershell
# Eliminar archivos persistentes
$appdata = $env:APPDATA
$updatePath = Join-Path $appdata "WindowsUpdate\update.exe"
if (Test-Path $updatePath) {
    Remove-Item $updatePath -Force
}

# Eliminar scripts temporales
$tempPath = $env:TEMP
Get-ChildItem $tempPath -Filter "*.vbs" -Recurse | Remove-Item -Force
```

### 3. Controles de Red
```powershell
# Bloquear dominios sospechosos
defender.exe /blocklist add "discord.com" "cdn.discordapp.com"

# Monitorear tráfico saliente
netsh advfirewall firewall add rule name="Bloquear Saliente Discord" dir=out action=block remoteip=discord.com cdn.discordapp.com
```

## 7. Respuestas a Incidentes

### Protocolo de Respuesta
1. **Contener**: Aislar sistema afectado
2. **Analizar**: Recopilar artifacts y evidencia
3. **Remediar**: Eliminar toda persistencia
4. **Recuperar**: Restaurar sistema limpio
5. **Prevenir**: Mejorar controles de seguridad

### Artefacts a Recopilar
- Logs del sistema y aplicaciones
- Registry hives
- Listas de procesos y threads
- Capturas de pantalla del sistema
- Capturas de red
- Historico de archivos modificados

## 8. Documentación Legal

**Nota**: Este proyecto es para entornos controlados y autorizados. Todas las actividades deben realizarse con autorización explícita.

**Restricciones Éticas**:
- Solo para VMs aisladas sin conectividad a internet
- No usar en sistemas de producción o de usuarios
- Mantenerse dentro de los límites de la investigación autorizada
- Seguir todas las leyes y regulaciones aplicables

**Requisitos Legales**:
- Obtener permiso explícito del propietario del sistema
- Documentar todos los hallazgos y acciones
- Mantener registros seguros de la investigación
- Reportar cualquier descubrimiento de seguridad crítico

**Recomendaciones de Compliance**:
- Realizar investigación solo con autorización explícita
- Documentar el alcance y objetivos de cada ejercicio
- Mantener datos de investigación seguros y cifrados
- Reportar cualquier uso no autorizado o accidental