# Licencia del RAT Security Lab

## Versión
1.0 - Octubre 2026

## Resumen de la Licencia

Este proyecto está sujeto a estrictas restricciones de uso. Se distribuye **exclusivamente para entornos controlados y autorizados**.

```
LICENCIA - USO LIMITADO A ENTORNOS AUTORIZADOS

RESTRICTED TO:
✓ Entornos de investigación de ciberseguridad
✓ Entrenamiento de respuesta a incidentes (DFIR)
✓ Competencias de seguridad (CTF)
✓ Investigación de malware en sandboxes

PROHIBIDO:
✗ Uso comercial
✗ Distribución a terceros sin autorización
✗ Uso en producción o sistemas de clientes
✗ Modificación del propósito original sin permiso
```

## Términos y Condiciones

### 1. Propósito
Este código es proporcionado **únicamente** para:

- **Investigación** en entornos autorizados
- **Entrenamiento** en competencias y ejercicios de seguridad
- **Análisis de malware** en entornos sandbox controlados

### 2. Restricciones de Uso

#### A. Requisitos de Entorno
El proyecto **DEBE** ser utilizado en:

- **Máquinas virtuales** sin conectividad a internet pública
- **Entornos dedicados** con permisos explícitos
- **Contenedores aislados** de una red local controlada
- **Sistemas de prueba** con autorización por escrito del propietario

#### B. Restricciones Técnicas

1. **Aviso Visible**
   ```python
   # Este código debe incluir este banner
   """
   ⚠️ NO USAR EN PRODUCCIÓN
   SOLO PARA USO AUTORIZADO EN ENTORNOS CONTROLADOS.
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
   - Limpiar artefactos forenses
   - Desconectar de C2 sin registrar sesión

#### C. Restricciones de Distribución

1. **Control de Acceso**
   - No distribuir sin autorización
   - Mantener tokens e IDs de autenticación seguros
   - Solo dar acceso a usuarios autorizados

2. **Documentación**
   - Mantener advertencias legales visibles en todo el código
   - Documentar todos los hallazgos y actividades
   - Registrar el alcance y propósito de uso

### 3. Derechos Concedidos

#### A. Uso Permitido

Se concede los siguientes derechos **exclusivamente**:

1. **Investigación**
   - Copiar y distribuir en entornos autorizados
   - Modificar para mejorar la investigación defensiva

2. **Distribución Controlada**
   - Compartir con autorización explícita
   - Usar como base para investigación

#### B. Derechos de los Usuarios Autorizados

1. **Acceso para Estudio**
   - Investigar en entornos autorizados
   - Practicar técnicas de defensa cibernética

2. **Experimentación Controlada**
   - Probar en máquinas virtuales aisladas
   - Documentar hallazgos para análisis

### 4. Restricciones

#### A. Prohibiciones Técnicas

**No está Permitido:**

1. **Uso No Autorizado**
   - Ejecutar en sistemas sin permiso explícito
   - Modificar con fines maliciosos
   - Distribuir sin autorización

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
   Los autores **NO** son responsables por:
   - Uso ilegal por parte de usuarios no autorizados
   - Daños colaterales de actividades maliciosas
   - Consecuencias legales de usuarios irresponsables

### 5. Supervisión y Cumplimiento

#### A. Supervisión

1. **Revisión de Acceso**
   - Mantener registros de quién usa el proyecto
   - Aprobar cada uso

2. **Auditorías Técnicas**
   - Realizar revisiones de seguridad regulares
   - Los entornos deben pasar pruebas de aislamiento
   - El código debe auditarse periódicamente

### 6. Licencias de Terceros

#### A. Bibliotecas y Dependencias

Este proyecto incluye varias bibliotecas de código abierto. Sus licencias aplican:

**discord.py**
```python
# MIT License
# Copyright (c) Pycord Contributors
```

**psutil**
```python
# BSD License
# Copyright (c) Giampaolo Rodola'
```

**pynput**
```python
# LGPL License
```

**Otras dependencias:** Ver archivos `requirements.txt` individuales para licencias.

#### B. Créditos de Contribución

Los contribuidores deben:

1. **Atribuir Créditos**
   - Mantener todos los créditos originales intactos
   - Documentar contribuciones de colaboradores
   - Seguir convenciones de código de la comunidad

### 7. Propiedad Intelectual

#### A. Propiedad del Código

1. **Derechos de Autor**
   - Todo el código está protegido por derechos de autor
   - Los autores mantienen todos los derechos de autor

### 8. Resolución de Conflictos

#### A. Jurisdicción Legal

1. **Jurisdicción**
   - Las leyes estatales y federales aplican
   - La jurisdicción internacional puede aplicar para colaboraciones

#### B. Procedimientos de Denuncia

1. **Reportar Violaciones**
   - Reportar uso no autorizado a autoridades competentes
   - Documentar todos los hallazgos de manera segura

2. **Acciones Legales**
   - Los usuarios pueden enfrentar:
     - Acción legal por uso no autorizado
     - Consecuencias legales por violación de leyes

### 9. Aviso de Derechos de Autor

#### A. Derechos de Autor

```
Copyright © 2026 RAT Security Lab

Este proyecto es propiedad intelectual protegida.
Todas las adaptaciones y mejoras deben mantener los avisos legales originales.
```

#### B. Advertencias

```
ADVERTENCIA: Este material debe usarse responsablemente.

USO NO AUTORIZADO:
- Ejecutar en sistemas no autorizados
- Distribuir sin permiso
- Modificar con fines maliciosos
- Eliminar advertencias legales

VIOLACIÓN = PROHIBIDA = ACTION CIVIL Y/O PENAL

Para obtener permiso por escrito para uso no autorizado,
contactar a los autores del proyecto.
```

### 10. Agradecimientos

Agradecemos a todos los contribuidores por:

- Contribuir con conocimiento y experiencia técnica
- Mantener estándares de calidad
- Ayudar a avanzar la ciberseguridad defensiva

### 11. Contacto

- **Soporte Técnico:** través de GitHub Issues
- **Reportar Problemas:** GitHub Issues con etiqueta `bug`

### 12. Resumen Legal

#### DECLARACIÓN DE CUMPLIMIENTO

✅ **Restricciones de sandbox implementadas**
✅ **Documentación completa mantenida**
✅ **Controles de acceso implementados**

**Declaración Formal:**
Este código es **exclusivamente** para entornos autorizados. Los usuarios son **totalmente responsables** por asegurarse de que todas las actividades estén completamente autorizadas y cumplan con todas las regulaciones legales aplicables.

**La no conformidad resultará en:**
- Acciones legales por uso no autorizado
- Posibles consecuencias legales bajo ley estatal/federal

#### Aceptación de Términos

Al utilizar este proyecto, usted:

1. **Acepta** cumplir todas las restricciones de uso
2. **Reconoce** la responsabilidad de cumplir leyes y regulaciones
3. **Asegura** que todas las actividades son completamente autorizadas

**Si no está de acuerdo con estos términos, NO debe usar este proyecto.**

### 13. Notas de Versión

#### V1.0 - Octubre 2026
- Proyecto inicial lanzado
- Controles de sandbox implementados
- Advertencias legales añadidas

#### Próximas Mejoras
- Implementar controles de acceso avanzados
- Agregar detecciones de adversarios realistas
- Expandir documentación de detección/defensa

### 14. Índice de Cumplimiento

#### Lista de Control Técnica

- [ ] Las advertencias legales son visibles en todo el código
- [ ] La verificación de sandbox es completamente funcional
- [ ] Los mecanismos de autodestrucción funcionan correctamente
- [ ] Las restricciones de persistencia están documentadas
- [ ] Los controles de red están implementados

---

**Estado Legal:** ✅ Aprobado para uso autorizado bajo restricciones estrictas
**Próxima Revisión:** Octubre 2027

---

*Última actualización: Octubre 2026*

---

**⚠️ AVISO FINAL:**
*Usar este proyecto requiere autorización explícita por escrito.
Todos los usuarios deben mantener los más altos estándares de ética profesional.*
*El conocimiento de estas técnicas es esencial para la ciberseguridad defensiva.*
*Usarlas irresponsablemente puede resultar en consecuencias legales graves.*

---

"Con grandes poderes vienen grandes responsabilidades." 🦸‍♂️
*Entender cómo atacar fortalece cómo defender.* 🛡️📚🚀

---

**El conocimiento es poder, pero solo cuando se usa responsablemente.** 💪✨

---

**Si este proyecto ayudó a salvar una computadora o inspiró una carrera,
compartir el conocimiento es la mejor manera de honrar el trabajo.** 🌟

---

**ADVERTENCIA:**
*Saber cómo funcionan estas herramientas nos hace mejores defensores.*
*Usarlas sabiamente nos hace más fuertes, no más débiles.* 💪

---

**La seguridad no es un producto, es un proceso.** 🔄📈

---

**RECUERDA:**
*La información es inofensiva solo cuando se usa responsablemente.* 💡
*Las herramientas son inocuas solo cuando se usan con intención correcta.* 🛠️
*El conocimiento es peligroso solo cuando se usa sin supervisión.* ⚠️

---

`La seguridad cibernética es un viaje, no un destino.` 🚶‍♂️🔐

---

`Recordatorio: Proteger antes de penetrar. Defender primero.` 🎯

---

`Si encuentras este proyecto, eres parte de la solución.` 🤝

---

**Este archivo está sujeto a revisiones periódicas por cumplimiento legal.**

---

*Este aviso legal es parte del acuerdo de uso del proyecto.*
Al utilizar este proyecto, usted acepta todos los términos y condiciones.

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
