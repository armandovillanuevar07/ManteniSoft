# ManteniSoft

## Sistema de Gestión de Mantenimiento

ManteniSoft es una aplicación web desarrollada en Python con Flask, orientada a la gestión de equipos y la programación y seguimiento de actividades de mantenimiento preventivo.

El proyecto busca facilitar el control de los equipos, organizar las actividades de mantenimiento y visualizar indicadores que permitan conocer el estado de las tareas programadas.

## Funcionalidades principales

### 1. Gestión de equipos
- Registrar equipos.
- Consultar los equipos registrados.
- Validar que no existan códigos duplicados.
- Almacenar la información en una base de datos SQLite.

### 2. Programación de mantenimientos
- Seleccionar un equipo registrado.
- Programar actividades de mantenimiento preventivo.
- Consultar las actividades programadas.
- Cambiar el estado de una actividad a completado.

### 3. Panel de seguimiento
- Visualizar el total de equipos registrados.
- Consultar el total de mantenimientos programados.
- Identificar mantenimientos pendientes.
- Consultar mantenimientos completados.
- Identificar mantenimientos vencidos.

## Tecnologías utilizadas

- Python 3.14
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML5
- CSS3
- pytest
- Git y GitHub
- GitHub Actions

## Estructura del proyecto

```text
ManteniSoft/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── templates/
│   └── static/
│       └── css/
├── tests/
│   └── test_app.py
├── docs/
│   ├── arquitectura.md
│   └── entornos.md
├── .github/
│   └── workflows/
│       └── tests.yml
├── config.py
├── requirements.txt
├── run.py
├── README.md
└── .gitignore
```

## Requisitos previos

- Python 3.14 o compatible.
- Git.
- pip.

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/armandovillanuevar07/ManteniSoft.git
```

### 2. Ingresar a la carpeta

```bash
cd ManteniSoft
```

### 3. Crear un entorno virtual

```bash
python3 -m venv .venv
```

### 4. Activar el entorno virtual

En macOS o Linux:

```bash
source .venv/bin/activate
```

### 5. Instalar las dependencias

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 6. Ejecutar la aplicación

```bash
python run.py
```

### 7. Abrir en el navegador

```text
http://127.0.0.1:5000/
```

## Configuración de entornos

ManteniSoft utiliza una configuración diferenciada para los entornos de desarrollo, pruebas y producción. La selección se realiza mediante la variable de entorno `FLASK_ENVIRONMENT`.

### Entorno de desarrollo

Es el entorno utilizado durante la construcción y modificación de la aplicación.

Es el entorno predeterminado cuando no se especifica otra configuración.

```bash
python run.py
```

En este entorno, el modo de depuración está habilitado (`DEBUG=True`).

### Entorno de pruebas

Se utiliza para ejecutar las pruebas automatizadas mediante pytest. Las pruebas emplean una base de datos SQLite en memoria, evitando modificar la base de datos habitual del proyecto.

```bash
python -m pytest -v
```

### Entorno de producción

Se configura con el modo de depuración deshabilitado (`DEBUG=False`).

Para seleccionar este entorno:

```bash
export FLASK_ENVIRONMENT=production
```

Se recomienda definir una clave secreta segura mediante una variable de entorno:

```bash
export SECRET_KEY="reemplazar-por-una-clave-segura"
```

Para iniciar la aplicación con esta configuración:

```bash
python run.py
```

Para volver al entorno de desarrollo en la terminal actual:

```bash
unset FLASK_ENVIRONMENT
```

**Nota:** La configuración de producción permite separar los parámetros de ejecución, pero no representa por sí sola un despliegue en un servidor externo. Para un despliegue real se requiere configurar un servidor de aplicaciones, almacenamiento persistente y las medidas de seguridad correspondientes.

## Pruebas automatizadas

Para ejecutar las pruebas del proyecto:

```bash
python -m pytest -v
```

El proyecto cuenta actualmente con cinco pruebas automatizadas para verificar la carga del panel principal, el registro de equipos, la programación de mantenimientos, la actualización de estados y los indicadores del sistema.

### Casos de prueba verificados

| Prueba | Resultado |
|---|---|
| Carga de la página principal | Aprobada |
| Registro de equipos | Aprobada |
| Programación de mantenimientos | Aprobada |
| Completar mantenimientos | Aprobada |
| Indicadores del panel | Aprobada |

**Resultado: 5 pruebas aprobadas de 5 ejecutadas.**

## Base de datos

ManteniSoft utiliza SQLite como sistema de almacenamiento. Las tablas se crean automáticamente cuando se inicia la aplicación.

Los modelos principales son:

- **Equipo:** almacena el código, nombre, área y fecha del último mantenimiento.
- **Mantenimiento:** registra el equipo asociado, la fecha programada, la descripción y el estado de la actividad.

## Integración continua (GitHub Actions)

El proyecto utiliza GitHub Actions para ejecutar automáticamente las pruebas de software cuando se realizan cambios en las ramas `main` y `develop`.

El flujo de integración continua realiza las siguientes actividades:

1. Descarga el código del repositorio.
2. Configura Python 3.14 en Ubuntu.
3. Instala las dependencias del proyecto.
4. Ejecuta las pruebas automatizadas mediante pytest.

### Resultado de integración continua

La primera ejecución del workflow **ManteniSoft CI** finalizó correctamente en GitHub Actions.

- Entorno: Ubuntu Linux.
- Python: 3.14.9.
- pytest: 9.2.0.
- Pruebas aprobadas: 5 de 5.
- Estado: Correcto.

## Documentación técnica

En la carpeta `docs/` se encuentran los documentos relacionados con:

- Arquitectura técnica de la aplicación.
- Descripción y diferenciación de los entornos de desarrollo, pruebas y producción.

## Estado del proyecto

Proyecto académico en desarrollo para el Producto Académico N.° 1.

## Autor

Armando Walter Villanueva Rojas

## Repositorio

[GitHub - ManteniSoft](https://github.com/armandovillanuevar07/ManteniSoft)

## Licencia

Proyecto desarrollado con fines académicos.
