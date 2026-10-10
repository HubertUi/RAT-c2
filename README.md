# RAT Educational Lab

## Descripción del Proyecto

Este es un **laboratorio educativo completo de ciberseguridad** diseñado para enseñar tanto técnicas ofensivas como defensivas en un entorno controlado y seguro. El laboratorio simula un escenario completo de Red Team vs Blue Team utilizando un Remote Access Trojan (RAT) que se comunica a través de Discord.

## Advertencia Legal

```
⚠️ LABORATORIO EDUCATIVO DE CIBERSEGURIDAD - RAT SECURITY LAB

⚠️ USO PROHIBIDO:
✗ Sistemas de producción sin autorización
✗ Redes corporativas o personales sin permiso
✗ Computadoras en internet sin consentimiento del propietario
✗ Actividades maliciosas o ilegales de cualquier tipo

✅ USO PERMITIDO:
✓ Laboratorios académicos en universidades
✓ Entornos de prueba aislados (VMs sin internet)
✓ Competencias de seguridad (CTF)
✓ Investigación de malware en sandboxes controlados
✓ Entrenamiento de respuesta a incidentes (DFIR)

🎯 ESENCIAL PARA:
• Analistas de malware
• Equipos de respuesta a incidentes (DFIR)
• Ingenieros de defensa cibernética
• Investigadores de seguridad
```

## Estructura del Proyecto

```
rat-educational-lab/
├── victim/                    # Payload del RAT (5 clases principales)
│   ├── modules/             # Módulos del payload
│   │   ├── environment.py   # Verificación de entorno y evasión
│   │   ├── persistence.py  # Técnicas de persistencia
│   │   ├── intelligence.py # Recopilación de inteligencia
│   │   ├── discord_c2.py    # Cliente C2 Discord
│   │   └── commands.py      # Ejecutor de comandos
│   ├── victim/             # Archivo principal del payload
│   │   └── client.py
│   ├── requirements.txt    # Dependencias del victim
│   └── README.md           # Documentación del victim
│
├── attacker/                # Centro de comando C2
│   ├── bot.py              # Bot principal de Discord
│   ├── commands.py         # Comandos del panel de control
│   ├── config.py           # Configuración
│   ├── requirements.txt    # Dependencias del atacante
│   └── README.md           # Documentación del atacante
│
├── docs/                    # Documentación educativa
│   ├── analisis_tecnnicas.md    # Análisis de técnicas utilizadas
│   └── contramedidas.md       # Guías de detección y remediación
│
├── LICENSE.md              # Aviso legal completo
└── README.md               # Este archivo (README principal)
```

## Componentes del Laboratorio

### 1. Payload del RAT (Victim)

#### Módulo 1: Verificación de Entorno (`modules/environment.py`)
- **Propósito:** Entender cómo el malware detecta sandboxes y evita análisis
- **Técnicas:**
  - Detección de usuarios/hostnames de sandbox
  - Detección de procesos de análisis (Wireshark, ProcMon, debuggers)
  - Verificación de recursos del sistema (RAM baja, pocos cores, uptime corto)
  - Detección de actividad de mouse (inusual en sandboxes)
- **Uso educativo:** Entender técnicas de evasión del malware real

#### Módulo 2: Persistencia (`modules/persistence.py`)
- **Propósito:** Implementar y detectar técnicas comunes de persistencia
- **Técnicas:**
  - Clave de registry Run (HKCU\Software\Microsoft\Windows\CurrentVersion\Run)
  - Carpeta de inicio con accesos directos
  - Tareas programadas con privilegios SYSTEM
  - Suscripciones WMI fileless (eventos al iniciar Windows)
- **Uso educativo:** Aprender cómo el malware mantiene acceso persistente

#### Módulo 3: Recopilación de Inteligencia (`modules/intelligence.py`)
- **Propósito:** Entender técnicas de reconocimiento post-explotación
- **Información recopilada:**
  - Información del sistema (plataforma, versión, arquitectura)
  - Información de red (IPs, interfaces, hostname)
  - Información del usuario (permisos, rutas)
  - Información del hardware (cores, RAM, discos)
  - Software instalado (para exploits adicionales)
  - Estado de seguridad (antivirus, firewall)
  - Información de navegadores (Chrome, Firefox, Edge)
  - Archivos sensibles encontrados en el sistema
  - Contraseñas WiFi guardadas
- **Uso educativo:** Entender lo que el malware recopila después de la explotación

#### Módulo 4: Cliente C2 Discord (`modules/discord_c2.py`)
- **Propósito:** Entender cómo los atacantes usan plataformas legítimas para C2
- **Características:**
  - Comunicación asíncrona con bot de Discord
  - Protocolo de comandos para el atacante
  - Envío de archivos y capturas de pantalla
  - System fingerprinting para el atacante
- **Uso educativo:** Entender arquitecturas C2 y exfiltración de datos

#### Módulo 5: Ejecutor de Comandos (`modules/commands.py`)
- **Propósito:** Entender capacidades típicas de RATs
- **Comandos implementados:**
  - `!help` - Mostrar comandos disponibles
  - `!info` - Información del sistema
  - `!shell <comando>` - Ejecutar comandos shell remotos
  - `!screenshot` - Capturar pantalla
  - `!download <archivo>` - Descargar archivos
  - `!upload` - Recibir archivos
  - `!ls <ruta>` - Listar archivos
  - `!cd <ruta>` - Cambiar directorio
  - `!cat <archivo>` - Ver contenido de archivo
  - `!processes` - Listar procesos activos
  - `!kill <pid>` - Terminar procesos
  - `!webcam` - Foto de webcam
  - `!record <segundos>` - Grabar audio
  - `!persist` - Establecer persistencia
  - `!elevate` - Intentar elevación de privilegios
  - `!shutdown` - Apagar sistema
  - `!reboot` - Reiniciar sistema
  - `!exit` - Cerrar sesión RAT
- **Uso educativo:** Entender capacidades típicas de RATs reales

#### Archivo Principal del Payload (`victim/client.py`)
- **Propósito:** Orquestar todos los módulos del RAT
- **Flujo:**
  1. **Fase 1 - Verificación de Entorno:** Detecta sandboxes y debuggers
  2. **Fase 2 - Evasión:** Delay aleatorio para evadir análisis automático
  3. **Fase 3 - Persistencia:** Establece todas las técnicas de persistencia
  4. **Fase 4 - Recopilación de Inteligencia:** Recopila información del sistema
  5. **Fase 5 - Conexión C2:** Conecta con bot Discord
  6. **Fase 6 - Loop de Comandos:** Escucha y ejecuta comandos del atacante

### 2. Centro de Comando (Attacker)

#### Bot Principal (`attacker/bot.py`)
- **Propósito:** Proporcionar interfaz de control al atacante
- **Características:**
  - Bot de Discord con todos los permisos necesarios
  - Comandos del panel: `!sessions`, `!broadcast`, `!cleanup`
  - Logging de todas las acciones para análisis forense
  - Sesiones activas rastreadas

#### Módulo de Comandos (`attacker/commands.py`)
- **Propósito:** Gestionar comandos del panel de control
- **Características:**
  - Gestión de sesiones activas
  - Comandos de broadcast a todas las víctimas
  - Herramientas de limpieza y mantenimiento
  - Logging de acciones del atacante

#### Configuración (`attacker/config.py`)
- **Propósito:** Gestionar configuración centralizada
- **Características:**
  - Variables de entorno para tokens y IDs
  - Esquema de validación
  - Configuración del servidor
  - Configuración de logging

### 3. Documentación Educativa

#### Documentación de Análisis (`docs/analisis_tecnnicas.md`)
- **Propósito:** Explicar en detalle cada técnica implementada
- **Contenido:**
  - Técnicas de evasión y anti-análisis
  - Múltiples vectores de persistencia
  - Métodos de reconocimiento post-explotación
  - Arquitecturas C2 vía Discord
  - Capacidades completas del RAT
  - Técnicas de evasión adicionales

#### Guía de Contramedidas (`docs/contramedidas.md`)
- **Propósito:** Proporcionar herramientas defensivas
- **Contenido:**
  - Técnicas de detección para cada amenaza
  - Scripts de detección automatizados
  - Guías de remediación
  - Protocolos de respuesta a incidentes
  - Reglas YARA y Sigma
  - Mejores prácticas de seguridad

### 4. Aviso Legal (`LICENSE.md`)
- **Propósito:** Garantizar uso ético y legal
- **Contenido:**
  - Restricciones estrictas de uso
  - Requisitos de entorno
  - Advertencias visibles en código
  - Procedimientos de supervisión
  - Contacto para soporte

## Instalación y Setup

### Prerrequisitos

1. **Crear entorno virtual (recomendado)**
```bash
python -m venv rat-lab-env
source rat-lab-env/bin/activate  # Linux/Mac
rat-lab-env\Scripts\activate     # Windows
```

2. **Instalar dependencias**
```bash
# Victim
pip install -r victim/requirements.txt

# Attacker  
pip install -r attacker/requirements.txt
```

### Configurar Variables de Entorno

#### Archivo .env (víctima)
```bash
# victim/.env
DISCORD_BOT_TOKEN=tu_token_del_bot_aqui
COMMAND_CHANNEL_ID=id_del_canal_aqui
RAT_ALLOW_SANDBOX=0  # 1 para testing en sandbox
```

#### Archivo .env (atacante)
```bash
# attacker/.env
DISCORD_BOT_TOKEN=tu_token_del_bot_aqui
COMMAND_CHANNEL_ID=id_del_canal_aqui
```

### Configurar Bot de Discord

1. **Crear aplicación**
   - Visitar: https://discord.com/developers/applications
   - Hacer clic en "New Application" → "Bot"
   - Copiar token del bot

2. **Configurar permisos**
   - Ir a OAuth2 → URL de autorización
   - Seleccionar canal de comandos
   - Copiar URL de invitación

3. **Configurar variables de entorno**
   - Ingresar token del bot
   - Ingresar ID del canal de comandos

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
# Navegar al directorio
mkdir -p rat-educational-lab/victim
cd rat-educational-lab/victim

# Instalar dependencias
pip install -r victim/requirements.txt

# Ejecutar RAT
python client.py --token "TU_TOKEN" --channel "ID_DEL_CANAL"

# Para testing en sandbox (solo VMs autorizadas)
python client.py --token "TU_TOKEN" --channel "ID_DEL_CANAL" --allow-sandbox
```

## Escenarios de Prueba

### Escenario 1: Detección de Sandbox
**Objetivo:** Entender cómo el malware detecta análisis

**Configuración:**
```bash
# Ejecutar en máquina virtual con nombres de sandbox
# (Esta es una máquina virtual educativa controlada)
```

**Resultado esperado:**
- RAT detecta sandbox
- Envía mensaje de "Entorno de análisis detectado"
- Termina ejecución si RAT_ALLOW_SANDBOX no está establecido

### Escenario 2: Análisis de Persistencia
**Objetivo:** Establecer y detectar técnicas de persistencia

**Técnicas a verificar:**
1. **Clave de registro Run**
2. **Acceso directo en carpeta de inicio**
3. **Tarea programada**
4. **Suscripción WMI**

**Verificar después de ejecución:**
```powershell
# En máquina víctima
Get-ItemProperty HKCU:\Software\Microsoft\Windows\CurrentVersion\Run
Get-ScheduledTask | Where-Object {$_.Actions.Execute -like "*update*"}
```

### Escenario 3: Monitor de Red
**Objetivo:** Capturar tráfico C2

**Herramientas:**
- Wireshark para captura de paquetes
- tcpdump para captura en línea
- Analizar tráfico HTTPS a Discord

### Escenario 4: Análisis Forense
**Objetivo:** Investigar artifacts del RAT

**Artefacts:**
- Claves de registro
- Tareas programadas
- Suscripciones WMI
- Archivos en %APPDATA%WindowsUpdate\*
- Capturas de pantalla
- Logs de actividades

## Ejemplo de Script de Setup

### setup_lab.py
```python
#!/usr/bin/env python3
"""
Script de configuración para el laboratorio educativo RAT
"""

import os
import subprocess
import sys
from pathlib import Path

def crear_estructuras():
    """Crea directorios y archivos necesarios"""
    os.makedirs("victim/modules", exist_ok=True)
    os.makedirs("attacker", exist_ok=True)
    os.makedirs("docs", exist_ok=True)
    print("✅ Estructuras creadas")

def instalar_dependencias():
    """Instala dependencias"""
    print("Instalando dependencias...")
    
    if os.path.exists("victim/requirements.txt"):
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "victim/requirements.txt"])
    
    if os.path.exists("attacker/requirements.txt"):
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "attacker/requirements.txt"])
    
    print("✅ Dependencias instaladas")

def crear_archivos_env():
    """Crea archivos .env de ejemplo"""
    # Victim .env
    victim_env = """# Configuración del Payload RAT (Víctima)
DISCORD_BOT_TOKEN=TU_TOKEN_DEL_BOT_AQUI
COMMAND_CHANNEL_ID=ID_DEL_CANAL_DE_DISCORD
RAT_ALLOW_SANDBOX=0  # Establecer a 1 para testing en sandbox
"""
    
    with open("victim/.env", "w") as f:
        f.write(victim_env)
    
    # Attacker .env
    attacker_env = """# Configuración del Bot C2 (Atacante)
DISCORD_BOT_TOKEN=TU_TOKEN_DEL_BOT_AQUI
COMMAND_CHANNEL_ID=ID_DEL_CANAL_DE_DISCORD
"""
    
    with open("attacker/.env", "w") as f:
        f.write(attacker_env)
    
    print("✅ Archivos .env creados")
    print("⚠️  IMPORTANTE: Editar .env con configuración real antes de ejecutar")

if __name__ == "__main__":
    print("🚀 Configurando laboratorio educativo RAT...")
    
    crear_estructuras()
    instalar_dependencias()
    crear_archivos_env()
    
    print("\n✅ Laboratorio listo para usar!")
    print("\n📋 Próximos pasos:")
    print("1. Configurar .env con tokens reales de Discord")
    print("2. Crear bot de Discord e invitarlo")
    print("3. Ejecutar atacante: cd attacker && python bot.py")
    print("4. Ejecutar víctima: cd victim && python client.py --token TOKEN --channel ID")
```

## Uso Educativo Recomendado

### Para Docentes

1. **Planificar laboratorios**
   - Usar scenarios de prueba como ejercicios guía
   - Crear laboratorios adicionales basados en este código
   - Diseñar evaluaciones prácticas

2. **Configurar entornos**
   - Preparar máquinas virtuales para ejecución del laboratorio
   - Configurar bots de Discord para el laboratorio
   - Establecer directorios de almacenamiento seguros

3. **Supervisar actividades**
   - Asegurarse de que todo uso sea autorizado
   - Monitorear logs de actividad
   - Documentar todos los hallazgos

### Para Estudiantes

1. **Ejecutar el laboratorio**
   - Seguir cuidadosamente las instrucciones de setup
   - Usar solo entornos autorizados
   - Documentar todas las observaciones

2. **Aprender conceptos**
   - Entender cómo cada módulo funciona
   - Investigar técnicas de defensa correspondientes
   - Practicar detección usando las guías de contramedidas

3. **Reportar problemas**
   - Informar cualquier issue técnico al instructor
   - Reportar uso no autorizado inmediatamente
   - Documentar hallazgos técnicos

### Para Investigadores

1. **Expandir el laboratorio**
   - Agregar nuevas técnicas de ataque
   - Desarrollar nuevas técnicas de detección
   - Crear laboratorios derivados para cursos específicos

2. **Contribuir al proyecto**
   - Enviar pull requests con mejoras
   - Reportar bugs y sugerencias
   - Colaborar con otros investigadores

## Contribución

### Cómo Contribuir

1. **Crear fork** del repositorio
2. **Clonar** en tu máquina local:
```bash
git clone https://github.com/[usuario]/rat-educational-lab.git
cd rat-educational-lab
```

3. **Crear rama** para tus cambios:
```bash
git checkout -b feature/nueva-tecnica
```

4. **Hacer commit** de tus cambios:
```bash
git add .
git commit -m "Agregar [descripción]"
git push origin feature/nueva-tecnica
```

5. **Crear pull request** en GitHub

### Reglas de Contribución

- Seguir convenciones de código (PEP 8)
- Agregar pruebas para nuevas funciones
- Documentar cambios en README.md
- Mantener advertencias legales visibles
- Usar nombres descriptivos para ramas

### Mejoras Sugeridas

#### Mejoras Técnicas

1. **Ofuscación del Código**
   - Agregar ofuscación adicional
   - Implementar string encoding
   - Usar técnicas anti-debugging

2. **Técnicas de Evasión**
   - Inyección de procesos (Process Doppelganger)
   - Técnicas fileless
   - Uso de APIs ocultas de Windows

3. **C2 Avanzado**
   - Implementar dead drops
   - Usar servicios legítimos para exfiltración
   - Agregar cifrado de tráfico

#### Mejoras Educativas

1. **Laboratorios Adicionales**
   - RATs con firmas digitales
   - Análisis de malware en memoria
   - Técnicas de APT avanzadas

2. **Herramientas de Detección**
   - Scripts YARA para identificar el malware
   - Reglas Sigma para SIEM
   - IOCs actualizados

## Créditos

### Autores

- **Creador principal:** [Nombre del autor]
- **Colaboradores:** [Lista de colaboradores]
- **Revisores:** [Lista de revisores]

### Agradecimientos

Agradecemos a todos los contribuidores por:

- Crear este laboratorio educativo valioso
- Contribuir conocimiento y experiencia técnica
- Mantener estándares de calidad académica
- Ayudar a avanzar la educación en ciberseguridad

## Licencia

Este proyecto está bajo **licencia educativa estricta** para uso académico únicamente. Consulte el archivo `LICENSE.md` para detalles completos.

## Contacto

### Para Soporte Técnico

- **Problemas:** soporte@university.edu
- **Bugs:** bug-report@university.edu
- **Preguntas:** helpdesk@university.edu

### Para Colaboración Académica

- **Investigación:** research@university.edu
- **Docentes:** faculty@university.edu
- **Estudiantes:** students@university.edu

### Para Reportar Problemas

1. **Problemas técnicos:** Usar GitHub Issues
2. **Preguntas académicas:** Contactar al instructor
3. **Uso no autorizado:** Reportar inmediatamente a seguridad

## Estado del Proyecto

### ✅ Completado

- [x] Módulo de verificación de entorno
- [x] Módulo de persistencia
- [x] Módulo de recopilación de inteligencia
- [x] Cliente C2 Discord
- [x] Ejecutor de comandos
- [x] Archivo principal del payload
- [x] Bot principal de Discord
- [x] Módulo de comandos del atacante
- [x] Configuración
- [x] Documentación completa
- [x] Aviso legal

### 🔄 Próximos Pasos

1. **Documentación de uso**
   - Agregar ejemplos de casos de uso
   - Crear guías paso a paso
   - Documentar mejores prácticas

2. **Mejoras técnicas**
   - Implementar más técnicas de evasión
   - Agregar detecciones más avanzadas
   - Mejorar la ofuscación del código

3. **Herramientas educativas**
   - Agregar laboratorios de práctica
   - Crear hojas de trucos
   - Desarrollar cuestionarios

## Última Actualización

Octubre 2026 - Versión 1.0

---

**Estado Actual:** Laboratorio completamente implementado y listo para uso educativo

**Próxima Revisión:** Octubre 2027

**Equipo de Desarrollo:** [Nombre del equipo]

---

### Nota Importante

Este laboratorio está **exclusivamente** para fines educativos. Todo uso debe ser en entornos **autorizados** y bajo **supervisión académica**. La no conformidad puede resultar en consecuencias académicas y legales.

**¡Feliz (y seguro) hacking!** 💻🔒

---

`#CiberseguridadEducativa #LaboratorioAutorizado #AprendizajeResponsable`

---

**Recordatorio:**
*Entender cómo estas herramientas funcionan es esencial para defenderlas.*
*Usarlas responsablemente nos hace más fuertes, no más débiles.* 🛡️

---

`La información es inofensiva solo cuando se usa responsablemente.` 💡
`Las herramientas son inocuas solo cuando se usan con intención correcta.` 🛠️
`El conocimiento es peligroso solo cuando se usa sin supervisión.` ⚠️

---

`La ciberseguridad es un viaje, no un destino.` 🚶‍♂️🔐

---

`Si encuentras este laboratorio, eres parte de la solución.` 🤝

---

**Este proyecto es parte del programa de ciberseguridad de la universidad.**

---

`#APRENDERAPRENDERAPRENDER #DEFENDERPRIMER# 🚀`