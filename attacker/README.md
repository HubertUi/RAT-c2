# Centro de Comando C2 del Atacante

## Descripción

Este es el componente del centro de comando (C2) del laboratorio educativo RAT. Proporciona a los estudiantes una interfaz de "Red Team" para controlar el payload de la víctima y analizar sistemas comprometidos.

## Advertencia Legal

```
⚠️ PANEL DE CONTROL DEL ATACANTE - C2 SECURITY LAB

USO PROHIBIDO:
✗ Ataques a sistemas sin autorización
✗ Robo de información personal o corporativa
✗ Interferencia con redes o servicios
✗ Distribución de malware o código malicioso

USO PERMITIDO:
✓ Laboratorios académicos de técnicas de ataque
✓ Simulación de respuesta a incidentes (DFIR)
✓ Competencias de seguridad (CTF)
✓ Entrenamiento defensivo en detección
✓ Investigación de técnicas de ciberataque

ESENCIAL PARA:
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

### Módulo de Comandos (`commands.py`)
- **Comandos del panel** del atacante
- **Gestión de sesiones** activas
- **Acciones de broadcast** a todas las víctimas
- **Herramientas de limpieza** y mantenimiento

### Configuración (`config.py`)
- **Variables de entorno** del bot
- **Configuración del servidor**
- **Configuración de logging**
- **Validación de configuración**

## Requisitos del Sistema

### Dependencias del Sistema (Atacante)
```bash
pip install -r attacker/requirements.txt

Dependencias principales:
- discord.py==2.3.2: Cliente Discord para C2
- python-dotenv==1.0.0: Variables de entorno
- pytest==7.4.0: Pruebas unitarias
- pytest-asyncio==0.21.0: Pruebas asíncronas
```

### Requisitos del Sistema

- **Sistema Operativo:** Linux, Windows o macOS
- **Python:** 3.8 o superior
- **Memoria:** 2GB RAM (mínimo)
- **Red:** Conectividad a internet (para Discord)

## Instalación y Configuración

### 1. Prerrequisitos
```bash
# Crear entorno virtual (recomendado)
python -m venv c2-lab-env
source c2-lab-env/bin/activate  # Linux/Mac
c2-lab-env\Scripts\activate     # Windows

# Instalar dependencias
pip install -r attacker/requirements.txt
```

### 2. Configurar Variables de Entorno
```bash
# Archivo .env en la raíz del proyecto
DISCORD_BOT_TOKEN="tu_token_del_bot_aqui"
COMMAND_CHANNEL_ID="id_del_canal_de_comandos_aqui"
```

### 3. Configurar Aplicación de Discord

#### Paso 1: Crear Aplicación
1. Visitar: https://discord.com/developers/applications
2. Hacer clic en "New Application"
3. Dar nombre: "RAT C2 Security Lab"
4. Hacer clic en "Bot" en Build section

#### Paso 2: Configurar Bot
1. En Bot settings:
   - Nombre de usuario: "Security Bot"
   - Descripción: "Laboratorio educativo C2 para fines académicos"

2. En OAuth2:
   - URL de redirección: `https://discord.com/api/oauth2_redirect`
   - Permisos del bot:
     - Leer mensaje
     - Enviar mensaje
     - Adjuntar archivos
     - Gestionar canales

#### Paso 3: Invitar Bot
```
https://discord.com/oauth2/authorize?client_id=TU_CLIENT_ID&scope=bot&permissions=PERMISSIONS
```

#### Paso 4: Configurar Variables de Entorno
```bash
export DISCORD_BOT_TOKEN="TU_TOKEN_DEL_BOT"
export COMMAND_CHANNEL_ID="ID_DEL_CANAL"
```

## Ejecución del Laboratorio

### Terminal 1 - Centro de Comando (Atacante)
```bash
# Navegar al directorio
mkdir -p rat-educational-lab/attacker
cd rat-educational-lab/attacker

# Instalar dependencias
pip install -r attacker/requirements.txt

# Ejecutar bot C2
python bot.py
```

### Terminal 2 - Víctima (Máquina Comprometida)
```bash
# En la máquina víctima (ejemplo usando victim del laboratorio)
cd rat-educational-lab/victim
pip install -r victim/requirements.txt

# Ejecutar RAT (ejemplo con configuración)
python client.py --token "TU_TOKEN_DEL_BOT" --channel "ID_DEL_CANAL"

# Para testing (usar solo en VMs autorizadas)
python client.py --token "TU_TOKEN_DEL_BOT" --channel "ID_DEL_CANAL" --allow-sandbox
```

## Comandos del Panel de Control

### Comandos Principales

| Comando | Uso | Descripción |
|---------|-----|-------------|
| `!sessions` | Ninguno | Lista todas las sesiones activas |
| `!broadcast <mensaje>` | `<mensaje>` | Envía mensaje a todas las sesiones |
| `!cleanup` | Ninguno | Limpia sesiones inactivas |
| `!info` | Ninguno | Muestra información del sistema del bot |

### Ejemplos de Uso

```bash
# Ver sesiones activas
!sessions

# Broadcast a todas las víctimas
!broadcast "⚠️ ALERTA: Ejercicio de seguridad activo"

# Limpiar sesiones inactivas  
!cleanup

# Información del sistema
!info
```

## Configuración y Desarrollo

### Configuración (`config.py`)

#### DiscordConfig
```python
@dataclass
class DiscordConfig:
    bot_token: str
    command_channel_id: int
    
    @classmethod
    def from_env(cls) -> 'DiscordConfig':
        """Crea configuración desde variables de entorno"""
        token = os.getenv('DISCORD_BOT_TOKEN')
        channel_id_str = os.getenv('COMMAND_CHANNEL_ID')
        
        if not token:
            raise ValueError("DISCORD_BOT_TOKEN no está definida")
        
        if not channel_id_str:
            raise ValueError("COMMAND_CHANNEL_ID no está definida")
        
        try:
            channel_id = int(channel_id_str)
        except ValueError:
            raise ValueError("COMMAND_CHANNEL_ID debe ser un número entero")
        
        return cls(
            bot_token=token,
            command_channel_id=channel_id
        )
```

#### AppConfig
```python
class AppConfig:
    """Configuración principal de la aplicación"""
    
    def __init__(self):
        self.discord = DiscordConfig.from_env()
        self.server = ServerConfig()
        self.logging = LoggingConfig()
    
    def validate(self):
        """Valida la configuración"""
        # Implementación de validación
        return True
```

### Pruebas

#### Ejemplo de Prueba Unitaria
```python
# tests/test_bot.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from attacker.bot import ControlCommands

@pytest.mark.asyncio
async def test_sessions_command():
    """Testea el comando de sesiones"""
    mock_bot = MagicMock()
    mock_bot.send = AsyncMock()
    
    commands = ControlCommands(mock_bot)
    await commands.sessions_command(mock_bot)
    
    mock_bot.send.assert_called_once_with("Sesiones activas")
```

#### Correr Pruebas
```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio

# Correr todas las pruebas
pytest

# Correr pruebas específicas
pytest tests/test_bot.py
```

## Monitoreo y Logs

### Logging de Actividades
El bot registra:

1. **Eventos de conexión**
   ```
   2024-10-08 10:30:15 - INFO - Bot iniciado: Security Bot
   2024-10-08 10:30:16 - INFO - Esperando conexiones...
   ```

2. **Sesiones de víctimas**
   ```
   2024-10-08 11:45:22 - INFO - Nueva sesión: ABC123DEF456
   2024-10-08 11:45:22 - INFO - Sesión iniciada desde: 192.168.1.100
   ```

3. **Comandos del atacante**
   ```
   2024-10-08 12:00:45 - INFO - Atacante: sessions - Admin: hacker
   2024-10-08 12:01:12 - INFO - Atacante: broadcast - Admin: hacker - Mensaje: ¡Ejercicio activo!
   ```

### File de Log
```
# attacker/logs/bot.log
2024-10-08 10:30:15,123 - INFO - Bot iniciado: Security Bot
2024-10-08 10:30:16,456 - INFO - Canal C2: #comando
2024-10-08 11:45:22,789 - INFO - Nueva sesión: ABC123DEF456
2024-10-08 12:00:45,123 - INFO - Atacante: sessions - Admin: hacker
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

## Guía de Mejora para Estudiantes

### Mejoras Técnicas

#### 1. Seguridad del Bot
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

#### 2. Detección Avanzada
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

#### 3. Autenticación del Panel
```python
# Agregar autenticación de dos factores
from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher = Fernet(key)
```

### Mejoras de Documentación

#### 1. Guía de Referencia Rápida
```markdown
# Referencia Rápida del Bot C2

## Comandos
- `!sessions`: Ver víctimas activas
- `!broadcast <msg>`: Enviar a todos
- `!cleanup`: Limpiar sesiones
- `!info`: Estado del sistema

## Configuración
- TOKEN: Token del bot Discord
- CHANNEL: ID del canal de comandos
- LOG_LEVEL: DEBUG, INFO, WARNING
```

#### 2. Documentación de API
```python
# api/endpoints.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(title="C2 Security Lab API")

@app.get("/api/sessions")
async def get_sessions():
    """Devuelve sesiones activas"""
    # Implementación
    return {"sessions": sessions}

@app.post("/api/broadcast")
async def broadcast_message(message: str):
    """Envía broadcast a todas las sesiones"""
    # Implementación
    return {"status": "success", "message": message}
```

## Contacto y Soporte

### Para Docentes

- **Problemas técnicos:** contactar al soporte técnico del laboratorio
- **Errores en contenido:** contactar al autor del curso
- **Actualizaciones del laboratorio:** enviar solicitud a maintainer@university.edu

### Para Estudiantes

- **Problemas de ejecución:** usar `#soporte` en Discord
- **Dudas teóricas:** preguntar en #academico
- **Errores de configuración:** usar `#ayuda-configuracion`

### Recursos de Apoyo

- [Documentación de Discord API](https://discord.com/developers/docs)
- [Python Discord.py](https://discordpy.readthedocs.io/)
- [Guía de Seguridad de Metasploit](https://docs.metasploit.com/)
- [Documentación de Respuesta a Incidentes SANS](https://www.sans.edu/courses/incident-response)

## Mantenimiento y Actualización

### Script de Actualización
```python
# scripts/update_lab.py
#!/usr/bin/env python3
"""
Script de actualización automática para el laboratorio C2
"""

import subprocess
import sys
from pathlib import Path

def actualizar_dependencias():
    """Actualiza todas las dependencias"""
    print("Actualizando dependencias...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "-r", "attacker/requirements.txt"])
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "-r", "victim/requirements.txt"])

def hacer_backup():
    """Crea backup del estado actual"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"backup_{timestamp}"
    
    subprocess.run(["cp", "-r", "attacker", backup_path])
    print(f"Backup creado en: {backup_path}")

if __name__ == "__main__":
    print("🔄 Actualizando laboratorio C2...")
    hacer_backup()
    actualizar_dependencias()
    print("✅ Laboratorio actualizado!")
```

### Guía de Contribución

#### Para Mejorar el Laboratorio

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

#### Estándares de Calidad

- **Calidad de Código:** PEP 8, tipos anotados, docstrings
- **Pruebas:** >80% de cobertura, pruebas unitarias
- **Documentación:** README completo, comentarios
- **Seguridad:** Sin tokens hardcodeados, logging seguro

## Última Actualización

Octubre 2026 - Versión 1.0 para Centro de Comando Educativo

---

**Para soporte técnico:** c2-support@university.edu
**Para preguntas académicas:** profesor@university.edu
**Para reportar bugs:** github issues

*Este laboratorio es parte del programa de Investigación de Seguridad Computacional de la Universidad.*

---

**⚠️ RECORDATORIO IMPORTANTE:**
*Este bot C2 es para fines académicos únicamente. Usar en sistemas sin autorización puede violar leyes y regulaciones. Mantener la supervisión académica y seguir todos los protocolos de seguridad requeridos.*

---

"Herramientas de ataque entendidas, defensas construidas.“ 💻🔐"

---

*Esta documentación está sujeta a cambios según evolucione el laboratorio.*

---

**UTENSILIO DE CONOCIMIENTO:**
*Entender cómo funcionan estas herramientas nos hace más fuertes defensas.*
**APRENDER → PROTEGER → AVANZAR** 📚🛡️🚀

---