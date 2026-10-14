# Resumen del Proyecto: RAT Security Lab

## Visión General

Proyecto completo de ciberseguridad que simula un escenario Red Team vs Blue Team utilizando un Remote Access Trojan (RAT) que se comunica a través de Discord.

## Estructura del Proyecto

```
rat-educational-lab/
├── victim/                    # Payload del RAT (6 módulos)
│   ├── modules/             # Módulos del payload
│   │   ├── __init__.py      # ✅ Paquete Python válido
│   │   ├── environment.py   # ✅ Verificación de entorno y evasión
│   │   ├── persistence.py   # ✅ Técnicas de persistencia
│   │   ├── intelligence.py  # ✅ Recopilación de inteligencia
│   │   ├── discord_c2.py    # ✅ Cliente C2 Discord
│   │   ├── commands.py      # ✅ Ejecutor de comandos
│   │   └── keylogger.py     # ✅ Keylogger (pynput)
│   ├── client.py           # ✅ Archivo principal del RAT
│   ├── requirements.txt    # ✅ Dependencias del victim
│   └── README.md           # ✅ Documentación del victim
│
├── attacker/                # Centro de comando C2
│   ├── bot.py              # ✅ Bot principal de Discord (todo integrado)
│   ├── .env                # Configuración (NO subir a git)
│   ├── requirements.txt    # ✅ Dependencias del atacante
│   └── README.md           # ✅ Documentación del atacante
│
├── docs/                    # Documentación técnica
│   ├── analisis_tecnicas.md    # ✅ Análisis de técnicas utilizadas
│   └── contramedidas.md       # ✅ Guías de detección y remediación
│
├── test_connection.py      # ✅ Test de conexión del bot
├── test_victim_modules.py  # ✅ Test de módulos (114 pruebas)
├── DISCLAIMER.md           # ✅ Aviso legal
├── LICENSE.md              # ✅ Licencia
└── README.md               # ✅ Documentación principal
```

## Componentes

### ✅ Componente 1: Payload del RAT (Victim)

#### Verificación de Entorno (`modules/environment.py`)
- **Técnicas implementadas:**
  - Detección de usuarios/hostnames de sandbox
  - Detección de procesos de análisis (Wireshark, ProcMon, debuggers)
  - Verificación de recursos del sistema (RAM baja, pocos cores, uptime corto)
  - Detección de actividad de mouse (inusual en sandboxes)
  - Detección de debugger (IsDebuggerPresent, PEB BeingDebugged)

#### Persistencia (`modules/persistence.py`)
- **Técnicas implementadas:**
  - Clave de registro Run (HKCU\Software\Microsoft\Windows\CurrentVersion\Run)
  - Persistencia en carpeta de inicio con accesos directos (WScript)
  - Tareas programadas con privilegios SYSTEM
  - Suscripciones WMI fileless (eventos al iniciar Windows)

#### Recopilación de Inteligencia (`modules/intelligence.py`)
- **Información recopilada:**
  - Información del sistema (plataforma, versión, arquitectura)
  - Información de red (IPs, interfaces, hostname)
  - Información del usuario (permisos, rutas, privilegios)
  - Información del hardware (cores, RAM, discos)
  - Software instalado
  - Estado de seguridad (antivirus, firewall)
  - Información de navegadores (Chrome, Firefox, Edge)
  - Archivos sensibles encontrados en el sistema
  - Contraseñas WiFi guardadas

#### Cliente C2 Discord (`modules/discord_c2.py`)
- **Características implementadas:**
  - Comunicación asíncrona con bot de Discord
  - Protocolo de comandos para el atacante
  - Envío de archivos y capturas de pantalla
  - System fingerprinting para el atacante
  - Gestión de sesiones y cola de comandos
  - Ignora mensajes de bots (previene cross-talk)

#### Ejecutor de Comandos (`modules/commands.py`)
- **Comandos implementados:**
  - `!help`, `!info`, `!shell`, `!screenshot`, `!download`, `!upload`
  - `!ls`, `!cd`, `!pwd`, `!cat`
  - `!processes`
  - `!keylog start/stop`, `!keylog_dump`
  - `!broadcast` (no-op)
  - `!persist`, `!exit`

#### Keylogger (`modules/keylogger.py`)
- **Características implementadas:**
  - Captura de teclas con pynput
  - Buffer thread-safe con threading.Lock
  - Detección de teclas especiales (Enter, Shift, Ctrl, etc.)
  - Estado con uptime y contador de teclas
  - Limpieza automática del buffer después del dump

#### Archivo Principal del Payload (`victim/client.py`)
- **Flujo implementado:**
  1. **Fase 1 - Verificación de Entorno:** Detecta sandboxes y debuggers
  2. **Fase 2 - Evasión:** Delay aleatorio para evadir análisis automático
  3. **Fase 3 - Persistencia:** Establece todas las técnicas de persistencia
  4. **Fase 4 - Recopilación de Inteligencia:** Recopila información del sistema
  5. **Fase 5 - Conexión C2:** Conecta con bot Discord
  6. **Fase 6 - Loop de Comandos:** Escucha y ejecuta comandos del atacante

### ✅ Componente 2: Centro de Comando (Attacker)

#### Bot Principal (`attacker/bot.py`)
- **Características implementadas:**
  - Bot de Discord con todos los permisos necesarios
  - Comandos del panel: `!sessions`, `!victim`, `!broadcast`, `!keylog_dump`, `!notify`, `!cleanup`, `!info`, `!help_c2`
  - Logging de todas las acciones para análisis forense
  - Sesiones activas rastreadas con IP, OS, usuario, admin
  - Notificaciones de nuevas víctimas
  - Manejo de errores de comandos

### ✅ Componente 3: Tests

#### Test de Módulos (`test_victim_modules.py`)
- **114 pruebas cubriendo:**
  - Imports de los 6 módulos
  - EnvironmentChecker (detección de sandbox/VM/debugger)
  - IntelligenceCollector (recopilación de info)
  - Keylogger (start/stop/buffer/clear)
  - CommandExecutor (todos los 17 handlers)
  - DiscordC2Client (estructura)
  - process_queue (cola asíncrona)

#### Test de Conexión (`test_connection.py`)
- Verifica conexión del bot a Discord
- Envío de mensajes al canal

### ✅ Componente 4: Documentación

#### Análisis de Técnicas (`docs/analisis_tecnicas.md`)
- Técnicas de evasión, persistencia, reconocimiento, C2

#### Guía de Contramedidas (`docs/contramedidas.md`)
- Técnicas de detección, scripts, reglas YARA/Sigma

### ✅ Componente 5: Aviso Legal (`DISCLAIMER.md`, `LICENSE.md`)
- Restricciones estrictas de uso
- Requisitos de entorno
- Advertencias visibles en código

## Instalación

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r victim/requirements.txt
pip install -r attacker/requirements.txt
```

### Configurar Variables de Entorno

#### Archivo .env (atacante)
```bash
# attacker/.env
DISCORD_BOT_TOKEN=tu_token_del_bot_aqui
COMMAND_CHANNEL_ID=id_del_canal_aqui
```

### Configurar Bot de Discord

1. **Crear aplicación** en https://discord.com/developers/applications
2. **Generar token** del bot
3. **Activar 3 intents:** Presence, Server Members, Message Content
4. **Invitar bot** al servidor con permisos de Administrator
5. **Configurar variables de entorno**

## Ejecución

### Terminal 1 - Centro de Comando (Atacante)
```bash
cd attacker
python bot.py
```

### Terminal 2 - Víctima (Máquina Comprometida)
```bash
cd victim

# Ejecutar RAT
python client.py --token "TU_TOKEN" --channel "ID_DEL_CANAL"

# Para testing en sandbox (solo VMs autorizadas)
python client.py --token "TU_TOKEN" --channel "ID_DEL_CANAL" --allow-sandbox
```

## Verificación

### Ejecutar Tests
```bash
# Test de módulos (114 pruebas)
python test_victim_modules.py

# Test de conexión
python test_connection.py
```

## Próximos Pasos

### Para Mejoras Futuras

1. **Agregar técnicas:** Considerar nuevas técnicas de ataque y defensa
2. **Mejorar documentación:** Agregar más ejemplos y casos de uso
3. **Implementar detecciones:** Agregar nuevas reglas de detección YARA/Sigma

## Resumen Técnico

### Estadísticas del Proyecto

- **Archivos Python:** 10
- **Archivos de documentación:** 5
- **Módulos:** 6
- **Tests:** 114
- **Técnicas implementadas:** 20+
- **Comandos:** 20+

### Características Clave

✅ **Detección de Sandbox:** Múltiples técnicas de evasión
✅ **Persistencia:** 4 vectores de persistencia diferentes
✅ **Reconocimiento:** Información completa del sistema
✅ **C2:** Comunicación asíncrona vía Discord
✅ **Keylogger:** Captura de teclas con pynput
✅ **Comandos:** Control completo del sistema comprometido
✅ **Tests:** 114 pruebas automatizadas
✅ **Documentación:** Guías completas de análisis y defensa
✅ **Legal:** Advertencias estrictas de uso

## Conclusión

Este proyecto proporciona un **entorno completo** para:

- **Investigadores:** Analizar malware y técnicas de ataque
- **Defensores:** Entender cómo piensan los atacantes
- **Analistas DFIR:** Practicar respuesta a incidentes

El proyecto sigue los **principios de seguridad por diseño**:
- Aislamiento en VMs autorizadas
- Advertencias visibles en todo el código
- Mecanismos de autodestrucción en sandboxes
- Documentación completa de procedimientos

---

**Estado del Proyecto:** ✅ COMPLETADO

---

`#EntenderCómoAtacarFortaleceCómoDefender` 🛡️

`#InformaciónInofensivaSoloCuandoSeUsaResponsablemente` 💡

`#LaSeguridadNoEsUnDestino,EsUnViaje` 🚶‍♂️🔐

`#SiEncuentrasEsteProyectoEresParteDeLaSolución` 🤝

`#DEFENDERPRIMER` 🚀
