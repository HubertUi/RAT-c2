# Análisis de Técnicas Utilizadas

## 1. Verificación de Entorno (Anti-Análisis)
**Objetivo:** Entender cómo el malware detecta sandboxes

Técnicas implementadas:
- **Detección de usuarios/hostnames**: Sandboxes usan nombres predecibles
- **Procesos de análisis**: Detecta Wireshark, ProcMon, debuggers
- **Recursos del sistema**: RAM baja, pocos cores, uptime corto
- **Actividad humana**: Verifica movimiento de mouse

**Contramedidas:**
- Usar nombres realistas en sandboxes
- Ocultar procesos de análisis
- Simular interacción humana
- Proveer recursos suficientes

## 2. Persistencia
**Objetivo:** Múltiples vectores de persistencia

Técnicas:
- **Registry Run keys**: Clásica pero detectable
- **Startup folder**: Visible para usuarios
- **Scheduled Tasks**: Más sigilosa, con privilegios SYSTEM
- **WMI Event Subscription**: Persistencia fileless avanzada

**Detección:**
- Monitor registry keys de autostart
- Revisar tareas programadas sospechosas
- Auditar suscripciones WMI: `Get-WmiObject -Class __EventFilter`

## 3. Recopilación de Inteligencia
**Objetivo:** Reconocimiento post-explotación

Información recolectada:
- System fingerprinting
- Enumeración de red
- Credenciales WiFi (en texto plano)
- Información de navegadores
- Software instalado (para exploits adicionales)

## 4. Comunicación C2 vía Discord
**Objetivo:** Uso de plataformas legítimas para C2

Ventajas para atacantes:
- Tráfico HTTPS legítimo
- Infraestructura confiable
- Fácil exfiltración de datos
- Comunicación bidireccional

**Detección:**
- Monitorear conexiones a Discord API desde procesos sospechosos
- Analizar tráfico HTTPS con SSL inspection
- Endpoint detection de procesos inusuales

## 5. Capacidades del RAT
Funciones típicas:
- Shell remota
- Transferencia de archivos
- Captura de pantalla/webcam
- Keylogging
- Ejecución de comandos
- Manipulación de archivos

**Técnicas de Evasión:**
1. **Delay aleatorio**: Evita detección automática
2. **Verificación de conectividad**: Solo opera si hay internet
3. **Fingerprinting de entorno**: Envía información para adaptación
4. **Técnicas anti-VM**: Múltiples checks de sandbox
5. **Atributos ocultos**: Archivos ocultos y ofuscados