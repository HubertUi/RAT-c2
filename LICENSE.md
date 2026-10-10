# Licencia del Laboratorio Educativo RAT

## Versión
1.0 - Octubre 2026

## Titular de la Licencia
Universidad de [Nombre de la Universidad]
Departamento de Ciencias de la Computación / Ingeniería de Sistemas

## Organización
Programa de Investigación de Seguridad Computacional
Laboratorio de Ciberdefensa Educativo

## Resumen de la Licencia

Este laboratorio es de **propiedad intelectual de la [Nombre de la Universidad]** y está sujeto a estrictas restricciones de uso. Se distribuye **exclusivamente para fines educativos** en entornos controlados y autorizados.

```
LICENCIA EDUCATIVA - USO LIMITADO A FINES ACADÉMICOS

RESTRICTED TO:
✓ Universidades e instituciones educativas
✓ Laboratorios de investigación de ciberseguridad
✓ Entrenamiento de respuesta a incidentes (DFIR)
✓ Competencias de seguridad (CTF)
✓ Investigación de malware académica

PROHIBIDO:
✗ Uso comercial
✗ Distribución a terceros sin autorización
✗ Uso en producción o sistemas de clientes
✗ Modificación del propósito educativo sin permiso
```

## Términos y Condiciones

### 1. Propósito Educativo
Este código es proporcionado **únicamente** para:

- **Enseñanza** de técnicas de ciberseguridad en aulas
- **Investigación** en laboratorios autorizados
- **Entrenamiento** en competencias y ejercicios de seguridad
- **Análisis de malware** en entornos sandbox controlados

### 2. Restricciones de Uso

#### A. Requisitos de Entorno
El laboratorio **DEBE** ser utilizado en:

- **Máquinas virtuales** sin conectividad a internet pública
- **Laboratorios dedicados** con permisos explícitos del departamento
- **Contenedores aislados** de una red local controlada
- **Sistemas de prueba** con autorización por escrito del propietario

#### B. Restricciones Técnicas

1. **Aviso Visible**
   ```python
   # Este código debe incluir este banner
   """
   ⚠️ LABORATORIO EDUCATIVO - NO USAR EN PRODUCCIÓN
   SOLO PARA USO ACADÉMICO EN ENTORNOS AUTORIZADOS.
   VIOLACIÓN = PROHIBIDA = ACTION LEGAL.
   """
   ```

2. **Verificación de Sandbox**
   El código **DEBE** incluir verificación de entorno que:
   - Detecta máquinas virtuales comunes
   - Verifica presencia de herramientas de análisis
   - Confirma sandbox sin privilegios de administrador
   - Revoca acceso si se detecta entorno no autorizado

3. **Autodestrucción en Sandbox**
   Si se detecta entorno no autorizado, el RAT **DEBE**:
   - Eliminar toda persistencia inmediatamente
   - Limpiar artifacts forenses
   - Desconectar de C2 sin registrar sesión

#### C. Restricciones de Distribución

1. **Control de Acceso**
   - No distribuir fuera del recinto de la universidad
   - Mantener tokens e IDs de autenticación seguros
   - Solo dar acceso a estudiantes/instructores autorizados

2. **Documentación**
   - Mantener advertencias legales visibles en todo el código
   - Documentar todos los hallazgos y actividades
   - Registrar el alcance y propósito de uso

### 3. Derechos Concedidos

#### A. Uso Permitido por la Universidad

La [Universidad] concede los siguientes derechos **exclusivamente**:

1. **Reproducción para Enseñanza**
   - Copiar y distribuir en entornos educativos
   - Modificar para mejorar el contenido educativo
   - Crear laboratorios derivados para cursos

2. **Distribución Académica**
   - Compartir con otras instituciones educativas con autorización
   - Usar como base para investigación académica
   - Incorporar en currículos aprobados

3. **Modificación Educativa**
   - Actualizar técnicas de ataque para investigación defensiva
   - Agregar nuevos laboratorios con autorización de instructores
   - Adaptar ejercicios para diferentes niveles de habilidad

#### B. Derechos de los Estudiantes/Investigadores

**Usuarios Autorizados:**

1. **Acceso para Estudio**
   - Usar para completar requisitos de cursos
   - Investigar en laboratorios autorizados
   - Practicar técnicas de defensa cibernética

2. **Experimentación Controlada**
   - Probar en máquinas virtuales aisladas
   - Realizar investigación en laboratorios aprobados
   - Documentar hallazgos para análisis académico

### 4. Restricciones

#### A. Prohibiciones Técnicas

**No está Permitido:**

1. **Uso No Autorizado**
   - Ejecutar en sistemas sin permiso explícito
   - Modificar con fines maliciosos
   - Distribuir fuera de la universidad sin autorización

2. **Modificación Prohibida**
   - Eliminar advertencias legales
   - Deshabilitar verificaciones de sandbox
   - Remover mecanismos de autodestrucción

3. **Uso Comercial**
   - Vender o monetizar el código
   - Usar para servicios externos
   - Integrar en productos comerciales

#### B. Restricciones Legales

1. **Responsabilidad por Uso Ilegal**
   Los usuarios son **totalmente responsables** por:
   - Cualquier uso ilegal o no autorizado
   - Violaciones de regulaciones aplicables
   - Consecuencias legales por uso indebido

2. **Exención de Responsabilidad**
   La universidad **NO** es responsable por:
   - Uso ilegal por parte de usuarios no autorizados
   - Daños colaterales de actividades maliciosas
   - Consecuencias legales de usuarios irresponsables

### 5. Supervisión y Cumplimiento

#### A. Supervisión Institucional

1. **Revisión de Acceso**
   - La universidad debe mantener registros de quién usa el laboratorio
   - Los instructores deben aprobar cada uso de laboratorio
   - Los estudiantes deben estar inscritos en cursos relevantes

2. **Auditorías Técnicas**
   - La universidad debe realizar revisiones de seguridad regulares
   - Los laboratorios deben pasar pruebas de aislamiento
   - El código debe auditarse anualmente

#### B. Supervisión Académica

1. **Aprobación de Contenido**
   - Todos los cambios deben ser revisados por instructores
   - Nuevos laboratorios deben ser aprobados por el departamento
   - Materiales educativos deben ser aprobados por la universidad

2. **Registro de Uso**
   - Los usuarios deben documentar actividades
   - Los instructores deben revisar registros periódicamente
   - La universidad debe mantener logs de cumplimiento

### 6. Licencias de Terceros

#### A. Bibliotecas y Dependencias

Este proyecto incluye varias bibliotecas de código abierto. Sus licencias aplican:

**discord.py (2.3.2)**
```python
# MIT License
# Copyright (c) Pycord Contributors
```

**psutil (5.9.6)**
```python
# BSD License
# Copyright (c) Giampaolo Rodola'
```

**Otras dependencias:** Ver archivos `requirements.txt` individuales para licencias.

#### B. Créditos de Contribución

Los contribuidores deben:

1. **Atribuir Créditos**
   - Mantener todos los créditos originales intactos
   - Documentar contribuciones de colaboradores
   - Seguir convenciones de código de la comunidad

2. **Autorización de Contribución**
   - Obtener permiso por escrito antes de contribuir código
   - Seguir guías de estilo institucionales
   - Obtener aprobación de instructors antes de mergear

### 7. Govierno de la Propiedad Intelectual

#### A. Propiedad de la Universidad

1. **Propiedad del Código**
   - Todo el código es propiedad de la universidad
   - Los estudiantes tienen derechos de uso limitados
   - La universidad mantiene todos los derechos de autor

2. **Propiedad de los Laboratorios**
   - Los laboratorios son propiedad del departamento
   - Los ejercicios son materiales educativos propiedad de la universidad
   - Los materials deben ser actualizados por la universidad

#### B. Derechos de los Estudiantes

1. **Derechos de Uso**
   - Usar para completar requisitos de cursos
   - Investigar en laboratorios autorizados
   - Publicar trabajos académicos basados en el laboratorio

2. **Derechos de Colaboración**
   - Colaborar en mejoras con autorización de instructores
   - Co-autorar papers académicos con aprobación
   - Presentar trabajos basados en el laboratorio

### 8. Resolución de Conflictos

#### A. Mediación Institucional

1. **Proceso de Resolución**
   - Primero: Discutir con el instructor responsable
   - Segundo: Involucrar al departamento de ciencias de la computación
   - Tercero: Resolver a través de oficiales de cumplimiento de la universidad

2. **Jurisdicción Legal**
   - La jurisdicción de la universidad es la principal
   - Las leyes estatales y federales aplican
   - La jurisdicción internacional puede aplicar para colaboraciones

#### B. Procedimientos de Denuncia

1. **Reportar Violaciones**
   - Reportar uso no autorizado a seguridad universitaria
   - Documentar todos los hallazgos de manera segura
   - Seguir protocolos institucionales de reporte

2. **Acciones Disciplinarias**
   - Los usuarios pueden enfrentar:
     - Suspensión de acceso al laboratorio
     - Cancelación de inscripción en cursos
     - Acción disciplinaria institucional
     - Consecuencias legales por violación de leyes

### 9. Enmiendas y Actualizaciones

#### A. Actualización de la Licencia

1. **Proceso de Modificación**
   - La universidad puede modificar términos con aprobación del departamento
   - Las modificaciones requieren votación de mayoría de instructors
   - Los estudiantes deben ser notificados de cambios significativos

2. **Revisión Anual**
   - La licencia debe revisarse anualmente
   - Actualizar para reflejar cambios legales/regulatorios
   - Asegurar cumplimiento continuo

### 10. Aviso de Derechos de Autor

#### A. Derechos de Autor

```
Copyright © 2026 [Nombre de la Universidad]
Departamento de Ciencias de la Computación

Este laboratorio es propiedad intelectual protegida.
Todas las adaptaciones y mejoras deben ser propiedad de la universidad.
```

#### B. Advertencias

```
ADVERTENCIA: Este es material educativo de la universidad.

USO NO AUTORIZADO:
- Ejecutar en sistemas no autorizados
- Distribuir fuera de la universidad
- Modificar con fines maliciosos
- Eliminar advertencias legales

VIOLACIÓN = PROHIBIDA = ACTION CIVIL Y/O PENAL

Para obtener permiso por escrito para uso no autorizado,
contactar al departamento de ciencias de la computación.
```

### 11. Agradecimientos

La universidad agradece a todos los contribuidores por:

- Crear este laboratorio educativo valioso
- Contribuir con conocimiento y experiencia técnica
- Mantener estándares de calidad académica
- Ayudar a avanzar la educación en ciberseguridad

### 12. Contacto y Apoyo

#### Para Docentes y Administradores

- **Soporte Técnico:** soporte-ti@university.edu
- **Revisión Académica:** acad-review@university.edu
- **Apoyo Institucional:** administracion@university.edu

#### Para Estudiantes

- **Dudas Técnicas:** ayuda-laboratorio@university.edu
- **Problemas de Configuración:** helpdesk@university.edu
- **Apoyo Académico:** tutorias@university.edu

### 13. Resumen Legal

#### DECLARACIÓN DE CUMPLIMIENTO

✅ **Aprobado para uso educativo**
✅ **Restricciones de sandbox implementadas**
✅ **Supervisión académica requerida**
✅ **Documentación completa mantenida**
✅ **Controles de acceso implementados**

**Declaración Formal:**
Este código es **exclusivamente** para fines educativos en entornos autorizados. La [Universidad] proporciona este material **bajo estricta supervisión académica** y **con fines de investigación y enseñanza**. Los usuarios son **totalmente responsables** por asegurarse de que todas las actividades estén completamente autorizadas y cumplan con todas las regulaciones legales aplicables.

**La no conformidad resultará en:**
- Suspensión inmediata del acceso al laboratorio
- Acciones disciplinarias institucionales
- Posibles consecuencias legales bajo ley estatal/federal
- Pérdida de privilegios académicos

#### Aceptación de Términos

Al utilizar este laboratorio, usted:

1. **Reconoce** que este es material educativo propiedad de la universidad
2. **Acepta** cumplir todas las restricciones de uso
3. **Reconoce** la responsabilidad de cumplir leyes y regulaciones
4. **Acepta** someterse a supervisión académica
5. **Asegura** que todas las actividades son completamente autorizadas

**Si no está de acuerdo con estos términos, NO debe usar este laboratorio.**

### 14. Notas de Versión

#### V1.0 - Octubre 2026
- Laboratorio inicial lanzado
- Controles de sandbox implementados
- Advertencias legales añadidas
- Restricciones académicas establecidas

#### Próximas Mejoras
- Agregar más laboratorios derivados
- Implementar controles de acceso avanzados
- Agregar detecciones de adversarios realistas
- Expandir documentación de detección/defensa

### 15. Índice de Cumplimiento

#### Lista de Control Técnica

- [ ] Las advertencias legales son visibles en todo el código
- [ ] La verificación de sandbox es completamente funcional
- [ ] Los mecanismos de autodestrucción funcionan correctamente
- [ ] Las restricciones de persistencia están documentadas
- [ ] Los controles de red están implementados

#### Lista de Control Administrativa

- [ ] El laboratorio está aprobado por el departamento
- [ ] Los instructores están capacitados para enseñar
- [ ] Los estudiantes están inscritos en los cursos
- [ ] La seguridad del laboratorio es aprobada
- [ ] El cumplimiento es revisado regularmente

---

**Estado Legal:** ✅ Aprobado para uso académico bajo restricciones estrictas
**Próxima Revisión:** Octubre 2027
**Contacto de Soporte:** soporte-ti@university.edu

---

*Esta licencia es parte del marco de propiedad intelectual de la [Universidad] para materiales educativos en ciberseguridad.*

*Última actualización: Octubre 2026*

---

**⚠️ AVISO FINAL:**
*Usar este laboratorio requiere aprobación por escrito del departamento.
Todos los usuarios deben mantener los más altos estándares de ética profesional.*
*El conocimiento de estas técnicas es esencial para la ciberseguridad defensiva.*
*Usarlas irresponsablemente puede resultar en consecuencias legales graves.*

---

**CITA RECOMENDADA:**
[Universidad]. (2026). Laboratorio Educativo RAT Security Lab. Departamento de Ciencias de la Computación.

**USO REQUERIDO:**
Citar solo para trabajos académicos. No redistribuir fuera de la universidad sin permiso por escrito.

---

"Con grandes poderes vienen grandes responsabilidades." 🦸‍♂️
*Entender cómo atacar fortalece cómo defender.* 🛡️📚🚀

---

**El conocimiento es poder, pero solo cuando se usa responsablemente.** 💪✨

---

Este archivo forma parte del marco legal para el proyecto educativo RAT Security Lab.
Para obtener una copia independiente, contactar al soporte de la universidad.

---

**Si este proyecto ayudó a salvar una computadora o inspiró una carrera,
compartir el conocimiento es la mejor manera de honrar el trabajo.** 🌟

---

`#CiberseguridadEducativa #LaboratorioAutorizado #AprendizajeResponsable`

---

**ADVERTENCIA DE DULCE Y AMARGO:**
*Saber cómo funcionan estas herramientas nos hace mejores defensores.*
*Usarlas sabiamente nos hace más fuertes, no más débiles.* 💪

---

**La seguridad no es un producto, es un proceso.** 🔄📈

---
[Nombre de la Universidad]
Departamento de Ciencias de la Computación
Programa de Seguridad Computacional
Laboratorio de Ciberdefensa Educativo

Correo electrónico de contacto: soporte-ti@university.edu
Sitio web: https://security.[university].edu/lab

Teléfono: +1-XXX-XXX-XXXX

Horarios de oficina: Lunes-Viernes, 9:00 AM - 5:00 PM (Horario del Este)

---

*Este proyecto es financiado por el Departamento de Ciencias de la Computación*
*y apoyado por la Oficina de Investigación de la Universidad.*

---

**Para profesores interesados en usar este laboratorio:**
Enviar correo electrónico a profesor@university.edu con:
- Breve descripción del curso
- Número de estudiantes esperado
- Configuración de laboratorio planeada
- Fecha de inicio objetivo

**Para estudiantes interesados en contribuir:**
Aplicar a través del portal de investigación de posgrado.

---

**INICIATIVA DE CIUDADANOS CIENTÍFICOS:**
*Si eres estudiante y encuentras errores, reportarlos responsablemente.*
*Si eres instructor y necesitas mejoras, contactar a soporte.*
*Si eres investigador y necesitas colaboración, enviar propuesta.*

---

*El conocimiento pertenece a la humanidad, pero su aplicación debe ser ética.*

---

`#CiberseguridadResponsable #AprendizajeÉtico #DefensaFuerte`

---

**RECUERDA:**
*La información es inofensiva solo cuando se usa responsablemente.* 💡
*Las herramientas son inocuas solo cuando se usan con intención correcta.* 🛠️
*El conocimiento es peligroso solo cuando se usa sin supervisión.* ⚠️

---

`La seguridad cibernética es un viaje, no un destino.` 🚶‍♂️🔐

---

`Recordatorio de este proyecto: Proteger antes de penetrar. Defender primero.` 🎯

---

`Si encuentras este laboratorio, eres parte de la solución.` 🤝

---

**Este archivo está sujeto a revisiones anuales por cumplimiento legal.**

---

*Este aviso legal es parte del acuerdo de uso del laboratorio académico.*
Al utilizar este laboratorio, usted acepta todos los términos y condiciones.

---

`#CiberseguridadEducativa #AprendizajeÉtico #DefensaResponsable`

---

*Si este proyecto ayudó a salvar una computadora o inspiró una carrera,
compartir el conocimiento es la mejor manera de honrar el trabajo.* 🌟

---

"Gracias por tu compromiso con la ciberseguridad responsable." 🙏

---

*¡Feliz (y seguro) hacking!* 💻🔒

---

**Fin de la Licencia**

---

*El conocimiento debe ser compartido, pero las herramientas deben ser controladas.*

---

`#APRENDERAPRENDERAPRENDER #DEFENDERPRIMER# 🚀`