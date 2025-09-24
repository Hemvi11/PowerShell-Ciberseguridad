# PowerShell-Ciberseguridad

¿Qué contiene?

Contiene dos scripts de PowerShell que cumplen funciones básicas de seguridad y administración del sistema. El primero está orientado a la validación de archivos y la detección de errores de acceso, mientras que el segundo se centra en la auditoría de usuarios locales para identificar posibles cuentas en desuso o con riesgo de mal uso.

¿Qué scripts se incluyen?

Validación de archivos:

Una función que verifica si un archivo existe en el sistema.

Incluye manejo de errores para situaciones en las que el archivo no está accesible (por permisos, ruta incorrecta, etc.).

Auditoría de usuarios locales:

Un script que lista a los usuarios locales registrados en el sistema.

Genera una alerta si detecta que alguna cuenta está deshabilitada o nunca ha iniciado sesión.

¿Qué tareas de ciberseguridad resuelven?

Validación de archivos: Permite comprobar la existencia y accesibilidad de archivos críticos, lo cual ayuda a identificar problemas de integridad, disponibilidad o permisos incorrectos que podrían ser aprovechados por un atacante.

Auditoría de usuarios: Ayuda a detectar cuentas que representan un riesgo de seguridad (deshabilitadas pero existentes, o que nunca han sido usadas y pueden ser explotadas). Esto contribuye a reforzar la administración de identidades y accesos en el sistema.

¿Qué aprendiste al desarrollarlos?

A implementar manejo de errores en PowerShell para evitar que un script falle ante situaciones inesperadas.

La importancia de validar archivos como una práctica de seguridad y control de integridad.

Cómo obtener y analizar información sobre usuarios locales en el sistema, relacionándola con políticas de seguridad.

Que incluso scripts sencillos pueden ser útiles como herramientas de auditoría y prevención de riesgos en ciberseguridad.
