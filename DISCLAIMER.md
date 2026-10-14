# Aviso Legal - RAT Security Lab

## Propósito

Este proyecto está diseñado para demostrar técnicas de ciberseguridad defensiva y ofensiva en entornos controlados. **NO** es una herramienta para actividades maliciosas.

## Alcance y Uso

### ✅ Uso Permitido

1. **Entornos Controlados**
   - Máquinas virtuales aisladas sin conexión a internet
   - Entornos de prueba dedicados con permisos explícitos
   - Entornos de desarrollo seguros

2. **Investigación de Seguridad**
   - Análisis de malware en sandbox
   - Investigación de técnicas de ataque
   - Desarrollo de contramedidas defensivas

3. **CTF y Competencias**
   - Juegos de captura de bandera (Capture The Flag)
   - Competencias de seguridad organizadas
   - Desafíos de hacking autorizados

### ❌ Uso Prohibido

1. **Sistemas No Autorizados**
   - Computadoras personales sin permiso explícito
   - Sistemas corporativos sin autorización
   - Dispositivos de IoT o industriales

2. **Redes en Producción**
   - Sistemas de producción críticos
   - Redes de clientes o usuarios
   - Servicios en línea activos

3. **Distribución Maliciosa**
   - Uso con fines criminales
   - Ataques a infraestructura esencial
   - Robo de información personal

4. **Actividades Ilegales**
   - Violación de privacidad
   - Acceso no autorizado a datos
   - Daño a sistemas informáticos

## Información Legal

### Marco Regulatorio

**Estados Unidos:**
- Computer Fraud and Abuse Act (CFAA)
- Digital Millennium Copyright Act (DMCA)
- Convención de Budapest sobre Delitos Cibernéticos

**Internacional:**
- Ley General de Protección de Datos (GDPR)
- Regulaciones de privacidad locales
- Tratados de cooperación jurídica

### Limitaciones Legales

**Solo para Investigación:**
- Todo uso debe ser con autorización explícita por escrito
- Debe documentarse el propósito y alcance de la investigación
- Solo en sistemas de propiedad o claramente autorizados

**Protecciones de Responsabilidad:**
- Las actividades deben ser completamente documentadas
- Se deben mantener registros seguros de todas las acciones

## Protocolos de Seguridad

### Requisitos Técnicos

1. **Aislamiento**:
   - VMs sin conexión a internet pública
   - Redes locales dedicadas y aisladas
   - Contenedores o máquinas virtuales separadas

2. **Documentación**:
   - Registros detallados de todas las actividades
   - Reportes de uso y hallazgos

3. **Control de Acceso**:
   - Permisos mínimos necesarios
   - Autenticación de dos factores para acceso
   - Auditorías regulares de actividad

### Buenas Prácticas

1. **Ética en Investigación**:
   - Solo realizar pruebas autorizadas
   - Documentar todos los hallazgos
   - Reportar bugs y vulnerabilidades responsables

2. **Seguridad de Datos**:
   - Cifrar cualquier información recopilada
   - No compartir findings con partes no autorizadas
   - Eliminar datos después de la investigación

3. **Transparencia**:
   - Conocer los límites legales de investigación
   - Documentar el propósito
   - Reportar cualquier descubrimiento accidental

## Responsabilidades

### del Usuario

- **Legal:** Asegurarse de que todas las actividades sean legales y autorizadas
- **Ético:** Mantener los principios éticos de la investigación
- **Técnico:** Implementar todas las medidas de seguridad requeridas

## Implementaciones de Seguridad

### Protecciones Implementadas

1. **Verificación de Entorno**:
   - Detección automática de sandboxes
   - Verificación de VM y debugger
   - Verificación de conectividad a internet

2. **Aviso visible**:
   ```python
   # Advertencia visible en el código
   """
   ⚠️ NO USAR EN PRODUCCIÓN
   Solo para entornos autorizados.
   """
   ```

3. **Modo de Autodestrucción**:
   ```python
   # Lógica de autodestrucción después de 24 horas
   if tiempo > 24h:
       establecer_persistencia_cleanup()
   ```

4. **Banner Requerido**:
   ```
   ╔═══════════════════════════════════════════════
   ║ RAT Security Lab v1.0                         ║
   ║                                                ║
   ║ SOLAMENTE PARA USO AUTORIZADO                  ║
   ║ EN ENTORNOS AISLADOS Y CONTROLADOS             ║
   ║                                                ║
   ║ INFRACCIÓN = PROHIBIDA = ACTION LEGAL         ║
   ╚═══════════════════════════════════════════════╝
   ```

## Contacto y Reportes

### Reporte de Problemas

Si encuentra problemas de seguridad:
1. Documentar todos los pasos realizados
2. No intentar soluciones sin autorización
3. Mantener registros seguros de todos los hallazgos

### Denuncias

Reportar uso no autorizado o ilegal:
- Autoridades de seguridad competentes
- Agentes de cumplimiento legales apropiados

## Modificación y Distribución

### Permisos de Modificación

1. **Investigación:** Adaptar para nuevos ejercicios de análisis
2. **Documentación:** Actualizar guías y documentación
3. **Corrección:** Corregir bugs y errores

### Restricciones

- No redistribuir a partes no autorizadas
- No vender o monetizar el código
- Mantener todos los avisos legales intactos

## Resumen de Cumplimiento Legal

✅ **Documentación completa de seguridad**
✅ **Avisos visibles de protección**
✅ **Mecanismos de autodestrucción implementados**

**Declaración Final:**
Todo uso debe seguir los principios de investigación responsable y permanecer dentro de los límites estrictamente definidos por la autorización y las regulaciones legales aplicables.

**Disclaimer:** El usuario final asume toda la responsabilidad legal por este código. Los autores no son responsables de usos no autorizados o ilegales de este software.

*Última actualización: Octubre 2026*
