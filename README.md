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
├── .github/
│   └── workflows/
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

1. Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
```

2. Ingresar a la carpeta:

```bash
cd ManteniSoft
```

3. Crear un entorno virtual:

```bash
python3 -m venv .venv
```

4. Activar el entorno virtual en macOS o Linux:

```bash
source .venv/bin/activate
```

5. Instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

6. Ejecutar la aplicación:

```bash
python run.py
```

7. Abrir en el navegador:

```text
http://127.0.0.1:5000/
```

## Pruebas automatizadas

Para ejecutar las pruebas del proyecto:

```bash
python -m pytest -v
```

El proyecto cuenta actualmente con cinco pruebas automatizadas para verificar la carga del panel principal, el registro de equipos, la programación de mantenimientos, la actualización de estados y los indicadores del sistema.

## Base de datos

ManteniSoft utiliza SQLite como sistema de almacenamiento. Las tablas se crean automáticamente cuando se inicia la aplicación.

## Estado del proyecto

Proyecto académico en desarrollo para el Producto Académico N.° 1.

## Autor

Armando Walter Villanueva Rojas

## Licencia

Proyecto desarrollado con fines académicos.