# Documentación de casos de prueba – ManteniSoft

## 1. Objetivo

Documentar ocho casos de prueba representativos del sistema ManteniSoft,
con el propósito de verificar el funcionamiento del registro de equipos,
la programación y finalización de mantenimientos, y el módulo de seguimiento.

## 2. Entorno de pruebas

- Aplicación: ManteniSoft.
- Framework: Flask.
- Lenguaje: Python 3.14.10.
- Base de datos de pruebas: SQLite en memoria.
- Herramienta: pytest.
- Cliente: Flask test_client.
- Archivo de pruebas: `tests/test_app.py`.

Cada prueba utiliza una base de datos independiente en memoria, preparada
mediante las fixtures `app` y `client`.

## 3. Casos de prueba

### CP-01: Registro correcto de un equipo

- Función automatizada: `test_registrar_equipo`.
- Tipo: Caja negra.
- Objetivo: comprobar que el sistema registre un equipo cuando se proporcionan
  todos los datos obligatorios.
- Datos de entrada:
  - Código: EQ-001.
  - Nombre: Bomba principal.
  - Área: Planta.
  - Fecha del último mantenimiento: 2026-10-15.
- Procedimiento:
  1. Enviar una solicitud POST a `/equipos`.
  2. Proporcionar los datos del equipo.
  3. Seguir la redirección y revisar la respuesta.
- Resultado esperado: respuesta HTTP 200 y presencia del código EQ-001
  en la página.
- Resultado obtenido: satisfactorio; la prueba verifica el código EQ-001
  en la respuesta.
- Estado: APROBADO.

### CP-02: Registro de equipo con campos vacíos

- Función automatizada: `test_registrar_equipo_campos_vacios`.
- Tipo: Caja negra.
- Objetivo: comprobar que el sistema impida registrar un equipo cuando
  falta un dato obligatorio.
- Datos de entrada:
  - Código: vacío.
  - Nombre: Bomba principal.
  - Área: Planta.
  - Fecha: 2026-10-15.
- Procedimiento:
  1. Enviar una solicitud POST a `/equipos`.
  2. Dejar vacío el campo código.
  3. Revisar el mensaje mostrado por la aplicación.
- Resultado esperado: mostrar el mensaje
  "Todos los campos son obligatorios."
- Resultado obtenido: satisfactorio; la prueba comprueba la presencia
  del mensaje de validación.
- Estado: APROBADO.

### CP-03: Registro de un código de equipo duplicado

- Función automatizada: `test_registrar_equipo_codigo_duplicado`.
- Tipo: Caja negra.
- Objetivo: verificar que el sistema no permita registrar dos equipos
  con el mismo código.
- Datos de entrada:
  - Primer equipo: EQ-001, Bomba principal.
  - Segundo equipo: EQ-001, Bomba secundaria.
- Procedimiento:
  1. Registrar el primer equipo.
  2. Intentar registrar otro equipo utilizando el mismo código.
  3. Revisar el mensaje de respuesta.
- Resultado esperado: mostrar el mensaje
  "Ya existe un equipo con ese código."
- Resultado obtenido: satisfactorio; la prueba comprueba el mensaje
  de duplicidad.
- Estado: APROBADO.

### CP-04: Programación correcta de un mantenimiento

- Función automatizada: `test_programar_mantenimiento`.
- Tipo: Caja negra.
- Objetivo: comprobar que se pueda programar un mantenimiento para
  un equipo previamente registrado.
- Datos de entrada:
  - Equipo: EQ-001.
  - Fecha programada: 2026-11-15.
  - Descripción: Inspeccion preventiva.
- Procedimiento:
  1. Registrar un equipo de prueba.
  2. Obtener su identificador.
  3. Enviar una solicitud POST a `/mantenimientos`.
  4. Revisar la respuesta.
- Resultado esperado: respuesta HTTP 200 y presencia de la descripción
  "Inspeccion preventiva".
- Resultado obtenido: satisfactorio; la prueba verifica que la descripción
  aparezca en la respuesta.
- Estado: APROBADO.

### CP-05: Programación de mantenimiento con fecha inválida

- Función automatizada: `test_programar_mantenimiento_fecha_invalida`.
- Tipo: Caja negra.
- Objetivo: verificar que el sistema valide el formato de la fecha
  antes de registrar un mantenimiento.
- Datos de entrada:
  - Equipo: EQ-001.
  - Fecha programada: fecha-invalida.
  - Descripción: Inspección preventiva.
- Procedimiento:
  1. Registrar un equipo de prueba.
  2. Obtener su identificador.
  3. Enviar una solicitud POST a `/mantenimientos` con una fecha inválida.
  4. Revisar el mensaje de respuesta.
- Resultado esperado: mostrar el mensaje
  "La fecha ingresada no es válida."
- Resultado obtenido: satisfactorio; la prueba comprueba la presencia
  del mensaje de validación.
- Estado: APROBADO.

### CP-06: Finalización de un mantenimiento

- Función automatizada: `test_completar_mantenimiento`.
- Tipo: Caja negra.
- Objetivo: comprobar que un mantenimiento pendiente pueda cambiar
  al estado Completado.
- Datos de entrada:
  - Equipo: EQ-001.
  - Fecha programada: 2026-11-15.
  - Descripción: Cambio de filtros.
  - Estado inicial: Pendiente.
- Procedimiento:
  1. Registrar un equipo de prueba.
  2. Crear un mantenimiento pendiente.
  3. Enviar una solicitud POST a la ruta de finalización del mantenimiento.
  4. Revisar la respuesta.
- Resultado esperado: respuesta HTTP 200 y presencia del estado
  "Completado".
- Resultado obtenido: satisfactorio; la prueba comprueba que el estado
  Completado aparezca en la respuesta.
- Estado: APROBADO.

### CP-07: Visualización de todos los mantenimientos

- Función automatizada: `test_seguimiento_muestra_todos`.
- Tipo: Caja negra.
- Objetivo: verificar que el módulo de seguimiento muestre los registros
  cuando se selecciona el filtro Todos.
- Datos de entrada:
  - Dos mantenimientos pendientes con fechas anteriores al día actual.
  - Un mantenimiento pendiente con fecha posterior al día actual.
  - Un mantenimiento con estado Completado.
  - Filtro: Todos.
- Procedimiento:
  1. Crear los registros de prueba.
  2. Consultar `/seguimiento?estado=Todos`.
  3. Verificar la presencia de las cuatro descripciones.
- Resultado esperado: mostrar los mantenimientos vencidos, pendientes
  y completados.
- Resultado obtenido: satisfactorio; la prueba comprueba que las cuatro
  descripciones estén presentes.
- Estado: APROBADO.

### CP-08: Filtrado de mantenimientos vencidos

- Función automatizada: `test_seguimiento_filtra_vencidos`.
- Tipo: Caja negra.
- Objetivo: comprobar que el filtro Vencido muestre únicamente los
  mantenimientos pendientes cuya fecha programada sea anterior al día actual.
- Datos de entrada:
  - Dos mantenimientos pendientes con fechas anteriores al día actual.
  - Un mantenimiento pendiente con fecha posterior al día actual.
  - Un mantenimiento con estado Completado.
  - Filtro: Vencido.
- Procedimiento:
  1. Crear los registros de prueba.
  2. Consultar `/seguimiento?estado=Vencido`.
  3. Comprobar qué descripciones aparecen y cuáles quedan excluidas.
- Resultado esperado: mostrar los dos mantenimientos vencidos y excluir
  el pendiente futuro y el completado.
- Resultado obtenido: satisfactorio; la prueba verifica la presencia de
  los dos registros vencidos y la ausencia de los otros dos.
- Estado: APROBADO.

## 4. Resumen de resultados

| Indicador | Resultado |
|---|---:|
| Casos documentados | 8 |
| Casos aprobados | 8 |
| Casos fallidos | 0 |
| Porcentaje de aprobación | 100 % |

Los ocho casos documentados corresponden a funciones automatizadas
existentes en `tests/test_app.py`.

En la última ejecución completa reportada del proyecto se obtuvieron
23 pruebas aprobadas, con 131 de 131 sentencias cubiertas (100 % de
cobertura de sentencias).

## 5. Observaciones

- Las pruebas utilizan una base de datos SQLite en memoria para evitar
  modificar los datos de desarrollo.
- Los casos de seguimiento utilizan fechas relativas al día de ejecución.
- La cobertura del 100 % corresponde a cobertura de sentencias, no
  necesariamente a cobertura de ramas.
- Los resultados documentados corresponden a las aserciones implementadas
  en las pruebas automatizadas.
