# Payload del RAT

## Descripción

Este es el componente víctima del RAT (Remote Access Trojan). **SOLO** para entornos controlados con autorización explícita.

## Advertencia Legal

```
⚠️ RAT SECURITY LAB

USO PROHIBIDO:
✗ Sistemas de producción sin autorización
✗ Redes corporativas o personales sin permiso explícito
✗ Computadoras en internet sin consentimiento del propietario
✗ Actividades maliciosas o ilegales de cualquier tipo

USO PERMITIDO:
✓ Entornos de prueba aislados (VMs sin internet)
✓ Competencias de seguridad (CTF)
✓ Investigación de malware en sandboxes controlados
✓ Análisis defensivo de técnicas de ataque

ESPECIALMENTE RELEVANTE PARA:
• Analistas de malware
• Equipos de respuesta a incidentes (DFIR)
• Ingenieros de defensa cibernética
• Investigadores de seguridad
```

## Componentes

### Módulos del Payload (6 Módulos)

1. **Módulo de Verificación de Entorno** (`modules/environment.py`)
   - Detección de sandbox y VM
   - Verificación de debugger
   - Técnicas de evasión
   - Fingerprinting del entorno

2. **Módulo de Persistencia** (`modules/persistence.py`)
   - Claves de registry (Run/RunOnce)
   - Persistencia en carpeta de inicio
   - Tareas programadas
   - Suscripciones WMI

3. **Módulo de Recopilación de Inteligencia** (`modules/intelligence.py`)
   - Información del sistema
   - Enumeración de red
   - Información del usuario
   - Datos de navegadores
   - Archivos sensibles

4. **Módulo C2 de Discord** (`modules/discord_c2.py`)
   - Comunicación con bot C2
   - Protocolo de comandos
   - Envío de archivos y capturas

5. **Módulo de Comandos** (`modules/commands.py`)
   - Ejecución remota de comandos
   - Gestión de archivos
   - Captura de pantalla
   - Control del sistema

6. **Módulo Keylogger** (`modules/keylogger.py`)
   - Captura de teclas con pynput
   - Buffer thread-safe
   - Detección de teclas especiales

### Archivo Principal

- **client.py**: Orquesta todos los módulos y maneja el ciclo de vida del RAT

## Requisitos del Sistema

### Dependencias
```bash
pip install -r requirements.txt

Dependencias principales:
- discord.py: Cliente C2 de Discord
- psutil: Monitoreo del sistema
- Pillow: Procesamiento de imágenes
- pyautogui: Control del mouse/teclado
- pynput: Keylogger
- python-dotenv: Variables de entorno
```

### Requisitos del Sistema

- **Windows 10/11** (Compatibilidad principal)
- **Permisos de Administrador** (para persistencia)
- **Conectividad a Internet** (para C2)

## Instalación y Configuración

### 1. Prerrequisitos
```bash
# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r victim/requirements.txt
```

### 2. Configurar Variables de Entorno
```bash
# Archivo .env en la raíz del proyecto
export DISCORD_BOT_TOKEN="tu_token_aqui"
export COMMAND_CHANNEL_ID="id_del_canal"
export RAT_ALLOW_SANDBOX="1"  # Solo para testing
```

### 3. Configurar Bot de Discord

1. **Crear aplicación**
   - Visitar: https://discord.com/developers/applications
   - Hacer clic en "New Application"
   - Agregar "Bot" en la sección Build

2. **Generar Token**
   - Ir a "Bot" → "Copy Token"
   - Guardar token de forma segura

3. **Invitar Bot**
   - En configuraciones OAuth2, agregar "bot"
   - Seleccionar canal de comandos
   - Copiar URL de invitación

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
python client.py --token "TU_TOKEN" --channel "ID_DEL_CANAL"

# Para testing en sandbox
python client.py --token "TU_TOKEN" --channel "ID_DEL_CANAL" --allow-sandbox
```

## Escenarios de Prueba

### 1. Detección de Sandbox
**Objetivo:** Entender cómo el malware detecta análisis

**Configuración:**
```bash
# Ejecutar en máquina virtual sin modificar nombres
echo "User=sandbox" >> /etc/environment
echo "Hostname=sandbox-vm" >> /etc/hostname
```

**Resultado Esperado:**
- RAT detecta sandbox
- Envía mensaje de "Entorno de análisis detectado"
- Termina ejecución si RAT_ALLOW_SANDBOX no está establecido

### 2. Análisis de Persistencia
**Objetivo:** Establecer y detectar técnicas de persistencia

**Técnicas Probadas:**
- Clave de registro Run
- Acceso directo en carpeta de inicio
- Tarea programada
- Suscripción WMI

**Verificar:**
```powershell
# En máquina víctima
Get-ItemProperty HKCU:\Software\Microsoft\Windows\CurrentVersion\Run
Get-ScheduledTask | Where-Object {$_.Actions.Execute -like "*update*"}
```

### 3. Monitor de Red
**Objetivo:** Capturar tráfico C2 y detectar patrones de comunicación

**Herramientas:**
- Wireshark para captura de paquetes
- tcpdump para captura en línea
- Analizar tráfico HTTPS a Discord

### 4. Análisis Forense
**Objetivo:** Investigar artefactos del RAT comprometido

**Artefactos:**
- Registro (claves Run)
- Tareas programadas
- Suscripciones WMI
- Archivos en %APPDATA%WindowsUpdate\*
- Capturas de pantalla

## Detección y Análisis Defensivo

### Guía de Análisis

1. **Verificar Procesos**
   ```powershell
   # Buscar procesos RAT sospechosos
   Get-Process | Where-Object {
       $_.MainWindowTitle -like "*Python*" -and
       $_.Description -like "*RAT*"
   }
   ```

2. **Revisar Registro**
   ```powershell
   # Claves de persistencia
   Get-ItemProperty HKCU:\Software\Microsoft\Windows\CurrentVersion\Run
   ```

3. **Monitor Tareas Programadas**
   ```powershell
   # Tareas sospechosas
   Get-ScheduledTask | Where-Object {
       $_.Actions.Execute -like "*update*" -or
       $_.Actions.Execute -like "*windows*"
   }
   ```

4. **Capturar Red**
   ```bash
   # Wireshark display filter
   tcp.port == 443 and (discord.com or cdn.discordapp.com)
   ```

## Recomendaciones de Mejora

### Técnicas Avanzadas

1. **Ofuscación del Código**
   - Añadir ofuscación adicional
   - Implementar string encoding
   - Usar técnicas anti-debugging

2. **Técnicas de Evasión**
   - Inyección de procesos (Process Doppelganger)
   - Técnicas fileless
   - Uso de APIs de Windows ocultas

3. **C2 Avanzado**
   - Implementar dead drops
   - Usar servicios legítimos para exfiltración
   - Agregar cifrado de tráfico

### Herramientas de Detección

1. **Reglas de Detección**
   - Scripts YARA para identificar este RAT
   - Reglas Sigma para SIEM
   - Indicadores de compromiso (IOCs)

2. **Análisis**
   - Análisis de malware en memoria
   - Implementar técnicas de APT para pruebas

## Recursos Adicionales

- [Metasploit Framework](https://www.metasploit.com/)
- [Cobalt Strike](https://cobaltstrike.com/)
- [SANS SEC565](https://www.sans.edu/courses/red-team-operations)
- [Offensive Security](https://www.offensive-security.com/)

## Licencia

Consulte el archivo `LICENSE.md` para detalles.

## Advertencia Importante

**RECUERDE:** Entender cómo funcionan estas herramientas es esencial para la ciberseguridad defensiva. Sin embargo, su uso indebido puede violar leyes y regulaciones. Solo use este RAT en entornos controlados y autorizados.

**Tenga cuidado:** El conocimiento de técnicas de ataque es una arma de doble filo. Úselo solo para fortalecer la seguridad, no para comprometer sistemas.

---

**DULCE O AMARGO?** 📚

*Entender herramientas de ataque fortalece nuestras defensas.
Usarlas responsablemente nos hace más fuertes, no más débiles.*

---
