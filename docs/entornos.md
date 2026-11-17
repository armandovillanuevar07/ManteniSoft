# Gestión de entornos de ManteniSoft

## 1. Introducción

ManteniSoft considera tres entornos para organizar el desarrollo, la validación y la futura ejecución de la aplicación. Esta separación permite controlar los cambios, verificar las funcionalidades y reducir el riesgo de introducir errores.

## 2. Entorno de desarrollo (Development)

Es el entorno utilizado para programar, modificar y ejecutar las funcionalidades de ManteniSoft.

- Sistema operativo: macOS.
- Arquitectura del equipo: Apple Silicon.
- Lenguaje: Python 3.14.10.
- Framework: Flask.
- Base de datos: SQLite.
- Editor: Visual Studio Code.
- Entorno virtual: `.venv`.
- Control de versiones: Git.
- Repositorio remoto: GitHub.

En este entorno se desarrollan y verifican localmente los cambios antes de integrarlos en la rama `develop`.

## 3. Entorno de pruebas (Testing)

Se utiliza para comprobar que las funcionalidades de ManteniSoft trabajen correctamente y que los cambios no afecten las funcionalidades existentes.

Características:

- Herramienta de pruebas: pytest.
- Complemento de cobertura: pytest-cov.
- Base de datos: SQLite en memoria.
- Ejecución local: `python -m pytest -v`.
- Ejecución con cobertura: `python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=100 -v`.
- Integración continua: GitHub Actions.

El proyecto cuenta con 23 pruebas automatizadas que verifican:

- Visualización del panel principal.
- Registro y validación de equipos.
- Programación de mantenimientos.
- Finalización de mantenimientos.
- Indicadores del panel.
- Visualización y filtrado del módulo Seguimiento.
- Validaciones de datos y manejo de registros inexistentes.
- Configuración de los entornos.
- Representación de los modelos.

Las pruebas utilizan una base de datos SQLite en memoria para mantener aislados los datos de prueba y evitar modificar la base de datos de desarrollo.

En la última ejecución local reportada se obtuvieron los siguientes resultados:

| Indicador | Resultado |
|---|---:|
| Pruebas automatizadas aprobadas | 23 |
| Pruebas fallidas | 0 |
| Sentencias cubiertas | 131 de 131 |
| Cobertura de sentencias | 100 % |

El porcentaje indicado corresponde a cobertura de sentencias y no necesariamente a cobertura de ramas.

## 4. Integración continua (CI)

ManteniSoft utiliza GitHub Actions para automatizar la validación del código.

El flujo configurado ejecuta las pruebas automatizadas cuando se realizan eventos de integración definidos en el repositorio, como los envíos a las ramas `main` y `develop`, y las solicitudes de integración dirigidas a dichas ramas.

El proceso contempla:

1. Obtener el código del repositorio.
2. Configurar Python 3.14.
3. Instalar las dependencias del archivo `requirements.txt`.
4. Ejecutar las pruebas con pytest y pytest-cov.
5. Verificar que la cobertura de sentencias alcance el mínimo configurado del 100 %.

Esta automatización permite detectar errores antes de integrar cambios en las ramas principales.

## 5. Entorno de producción (Production)

Representa el entorno destinado a utilizar la aplicación de manera estable.

Para una futura implementación se consideran las siguientes características:

- Configuración de Flask con el modo de depuración desactivado.
- Uso de variables de entorno para proteger las claves de configuración.
- Base de datos persistente.
- Instalación de dependencias mediante `requirements.txt`.
- Despliegue en un servidor compatible con aplicaciones Python.
- Configuración de medidas de seguridad y respaldo de información.

El despliegue en producción queda planteado como una etapa posterior del proyecto académico. Por tanto, no se considera una implementación realizada.

## 6. Flujo de trabajo y control de versiones

El desarrollo utiliza Git y GitHub para administrar los cambios del proyecto.

El flujo de trabajo contempla:

1. Crear ramas `feature` para desarrollar funcionalidades específicas.
2. Realizar y probar los cambios en el entorno local.
3. Integrar las funcionalidades en `develop` mediante solicitudes de integración (Pull Requests).
4. Ejecutar las validaciones automatizadas mediante GitHub Actions.
5. Integrar en `main` las versiones que hayan sido revisadas y validadas.

Este procedimiento permite mantener organizados los cambios y disponer de una versión estable del proyecto.

## 7. Conclusión

La separación de entornos y el uso de integración continua permiten organizar el desarrollo de ManteniSoft, verificar sus funcionalidades y controlar la calidad del código. Asimismo, la documentación establece las condiciones necesarias para una futura implementación en producción.