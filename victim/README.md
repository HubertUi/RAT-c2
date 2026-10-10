# Payload del RAT Educativo

## Descripción

Este es el componente víctima del laboratorio educativo RAT (Remote Access Trojan). **SOLO** para fines académicos y de investigación en entornos controlados.

## Advertencia Legal

```
⚠️ LABORATORIO EDUCATIVO DE CIBERSEGURIDAD - RAT SECURITY LAB

USO PROHIBIDO:
✗ Sistemas de producción sin autorización
✗ Redes corporativas o personales sin permiso explícito
✗ Computadoras en internet sin consentimiento del propietario
✗ Actividades maliciosas o ilegales de cualquier tipo

USO PERMITIDO:
✓ Laboratorios académicos en universidades
✓ Entornos de prueba aislados (VMs sin internet)
✓ Competencias de seguridad (CTF)
✓ Investigación de malware en sandboxes controlados
✓ Análisis defensivo de técnicas de ataque

ESENCIAL PARA:
• Analistas de malware
• Equipos de respuesta a incidentes (DFIR)
• Ingenieros de defensa cibernética
• Investigadores de seguridad
```

## Componentes

### Módulos del Payload (5 Clases Principales)

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
   - Captura de pantalla/webcam
   - Control del sistema

### Archivo Principal

- **client.py**: Orquesta todos los módulos y maneja el ciclo de vida del RAT

## Requisitos del Sistema

### Dependencias del Sistema (Victim)
```bash
pip install -r requirements.txt

Dependencias principales:
- discord.py==2.3.2: Cliente C2 de Discord
- psutil==5.9.6: Monitoreo del sistema
- Pillow==10.1.0: Procesamiento de imágenes
- pyautogui==0.9.54: Control del mouse/teclado
- pyscreeze==0.1.30: Captura de pantalla
- python-dotenv==1.0.0: Variables de entorno
- colorama==0.4.6: Consola con colores
- requests==2.31.0: Conectividad de red
```

### Requisitos del Sistema

- **Windows 10/11** (Compatibilidad principal)
- **DirectX 11+** (para pyautogui)
- **Permisos de Administrador** (para persistencia)
- **Conectividad a Internet** (para C2 y updates)

## Instalación y Configuración

### 1. Prerrequisitos
```bash
# Crear entorno virtual (recomendado)
python -m venv rat-lab-env
source rat-lab-env/bin/activate  # Linux/Mac
rat-lab-env\Scripts\activate     # Windows

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

4. **Configurar**
```bash
# En variables de entorno
export DISCORD_BOT_TOKEN="TU_TOKEN_AQUI"
export COMMAND_CHANNEL_ID="123456789012345678"
```

## Ejecución del Laboratorio

### Terminal 1 - Centro de Comando (Atacante)
```bash
# En la máquina del atacante
mkdir attacker
cd attacker
pip install -r attacker/requirements.txt
python bot.py
```

### Terminal 2 - Víctima (Máquina Comprometida)
```bash
# En la máquina víctima (aislada)
mkdir victim
cd victim
pip install -r victim/requirements.txt

# Ejecutar RAT (ejemplo con configuración)
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
**Objetivo:** Investigar artifacts del RAT comprometido

**Artefacts:**
- Registro (claves Run)
- Tareas programadas
- Suscripciones WMI
- Archivos en %APPDATA%WindowsUpdate\*
- Capturas de pantalla
- Logs de actividades

## Script de Pruebas Automatizado

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
    # Directorios
    os.makedirs("victim/modules", exist_ok=True)
    os.makedirs("attacker", exist_ok=True)
    os.makedirs("docs", exist_ok=True)
    
    print("✅ Estructuras creadas")

def instalar_dependencias():
    """Instala dependencias"""
    print("Instalando dependencias...")
    
    # Victim
    if os.path.exists("victim/requirements.txt"):
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "victim/requirements.txt"])
    
    # Attacker
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

### Mejoras Técnicas

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

### Mejoras Educativas

1. **Laboratorios Adicionales**
   - Implementar RATs con firmas digitales
   - Agregar análisis de malware en memoria
   - Implementar técnicas de APT

2. **Herramientas de Detección**
   - Scripts YARA para identificar este RAT
   - Reglas Sigma para SIEM
   - Indicadores de compromiso (IOCs)

3. **Evaluación del Curso**
   - Guías de solución de laboratorios
   - Cuentas regresivas de tiempo de respuesta a incidentes
   - Simulaciones de respuesta a incidentes completas

## Contacto y Soporte

### Para Docentes

- Problemas con laboratorios: contactar al soporte técnico institucional
- Errores en contenido: contactar al autor del curso
- Falta de permisos: coordinar con administración IT

### Para Estudiantes

- Problemas técnicos: pedir ayuda al instructor
- Conceptos no claros: pedir explicación adicional
- Uso no autorizado: contactar al laboratorio inmediatamente

### Recursos Adicionales

- [Metasploit Framework](https://www.metasploit.com/)
- [Cobalt Strike](https://cobaltstrike.com/)
- [SANS SEC565](https://www.sans.edu/courses/red-team-operations)
- [Offensive Security](https://www.offensive-security.com/)

## Licencia

Este código es **exclusivamente para fines educativos**. Consulte el archivo `LICENSE.md` para detalles específicos.

## Advertencia Importante

**RECUERDE:** Entender cómo funcionan estas herramientas es esencial para la ciberseguridad defensiva. Sin embargo, su uso indebido puede violar leyes y regulaciones. Solo use este laboratorio en entornos controlados, autorizados, y bajo supervisión académica directa.

**Tenga cuidado:** El conocimiento de técnicas de ataque es una arma de doble filo. Úselo solo para fortalecer la seguridad, no para comprometer sistemas.

## Última Actualización

Octubre 2026 - Versión 1.0 para Laboratorio Académico

---

**Para soporte técnico:** [support@university.edu]
**Para preguntas académicas:** [profesor@university.edu]
**Para problemas legales:** [oficina-legal@university.edu]

*Este laboratorio es parte del programa de Ciberseguridad de la Universidad.*

---

**DULCE O AMARGO?** 📚

*El aprendizaje de herramientas de ataque fortalece nuestras defensas.
Usarlas responsablemente nos hace más fuertes, no más débiles.*

---