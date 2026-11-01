
# Gestión de entornos de ManteniSoft

## 1. Introducción

ManteniSoft considera tres entornos para organizar el desarrollo, la validación y la ejecución de la aplicación. Esta separación permite controlar los cambios y reducir el riesgo de introducir errores.

## 2. Entorno de desarrollo (Development)

Es el entorno utilizado para programar y modificar las funcionalidades de ManteniSoft.

- Sistema operativo: macOS.
- Lenguaje: Python 3.14.
- Framework: Flask.
- Base de datos: SQLite.
- Editor: Visual Studio Code.
- Entorno virtual: .venv.

En este entorno se desarrollan y verifican localmente los cambios antes de integrarlos en la rama develop.

## 3. Entorno de pruebas (Testing)

Se utiliza para comprobar que las funcionalidades trabajan correctamente.

- Herramienta de pruebas: pytest.
- Base de datos: SQLite en memoria.
- Ejecución: python -m pytest -v.
- Integración continua: GitHub Actions.

Las pruebas verifican el acceso a la página principal, el registro de equipos, la programación de mantenimientos, la finalización de mantenimientos y los indicadores del panel.

Actualmente se cuenta con cinco pruebas automatizadas aprobadas.

## 4. Entorno de producción (Production)

Representa el entorno destinado a utilizar la aplicación de manera estable.

Para una futura implementación se consideran las siguientes características:

- Configuración de Flask con modo de depuración desactivado.
- Uso de variables de entorno para proteger las claves de configuración.
- Base de datos persistente.
- Instalación de dependencias mediante requirements.txt.
- Despliegue en un servidor compatible con aplicaciones Python.

El despliegue en producción queda planteado como una etapa posterior del proyecto académico.

## 5. Flujo de trabajo

Los cambios se desarrollan en ramas feature, se integran en develop y se validan mediante las pruebas automatizadas. Una vez comprobada su estabilidad, los cambios pueden integrarse en main como versión estable.

## 6. Conclusión

La separación de entornos permite organizar el desarrollo de ManteniSoft, validar sus funcionalidades y establecer una base para su futura puesta en producción.
