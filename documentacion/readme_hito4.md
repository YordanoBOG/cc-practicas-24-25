Hito 4: Composición de servicios

Implementar aplicación (map) de puertos, interna y externa, de forma que se puedan usar y testear los servicios DÍA 3

Preparar un test que construya el cluster de contenedores y más tests para testear la API que se ejecuta en los contenedores. Tras eso, el contenedor se deberá subir a GitHub container registry. Esto deberá suceder con cada push. DÍA 3

Hacer documentación DÍA 5

--------------------------------------------------------------------------------

Descripción

Un contenedor es una de las formas estándar hoy en día para crear despliegues repetibles de cualquier tipo de aplicación. Cuando una aplicación no cabe en un solo contenedor por la existencia de varios tier (qué es un tier? Ni lo sé ni me importa, solo usa docker compose), o simplemente nodos que sirven para almacenar datos, es necesario usar Docker compose para describir de forma repetible la relación que tales contenedores tienen entre sí. Básicamente aquí te están diciendo que uses docker compose.

En esta práctica se trata de diseñar, usando docker compose y describiendo la infraestructura mediante un fichero compose.yaml (se crea un nuevo yaml que debe ejecutarse después del testeo de la API), un servicio que incluya MÍNIMO TRES (esto es requisito de la profesora) contenedores: para datos, para logs (que también almacenará los datos correspondientes a los logs de forma no volátil) y para la aplicación propiamente dicha, que en tu caso será la API de GeneSys (Puede ser que a ti te interese una BD de tipo MongoDB para almacenar los ficheros con los datos a emplear, más los workflows json. Y junto a eso, en la BD metes también la gestión de los usuarios).

El principal objetivo del uso de Docker u otro sistema de gestión de contenedores es aislar la ejecución de una aplicación de forma que sea mucho más fácil desplegarla, incluyendo los datos y el estado en el que se encuentre en un momento determinado; también permite crear fácilmente infraestructuras que se pueden reproducir en cualquier servicio o proveedor en la nube.

Se requiere el diseño de un Dockerfile para el contenedor de la aplicación (solo el de la aplicación) que se tendrá que subir al repositorio público. Generalmente, si se usa un solo contenedor es suficiente con un Dockerfile para gestionar la lógica del contenedor. Pero como usaremos varios, habrá que orquestarlos usando la aplicación docker compose.

En este hito tendrán que llevarse a la práctica diferentes conceptos relacionados con la composición de servicios.
    Creación de un contenedor con la aplicación desarrollada en los hitos anteriores (la API de GeneSys).
    Uso de contenedores de datos (o volúmenes), que permitan componer de forma variable las fuentes de datos que se van a usar en un clúster (o grupo de servicios) determinado.
    Aplicación (map) de puertos, interna y externa, de forma que se puedan usar y testear los servicios.
    Configuración del clúster para que todos los contenedores tengan la configuración que necesitan.
    Configuración-como-código, para que los servicios sean capaces de arrancar correctamente independientemente del entorno en el que se encuentren (un clúster, una instancia, o un test local).

La creación de un contenedor contiene varias fases:
    Elección de un contenedor base. Siempre habrá diferentes opciones, tanto si optamos por el "oficial" de un lenguaje (Si uso Python, pues un contenedor estándar de Python, que en principio debería ejecutar los scripts en bash sin problema porque viene montado sobre Debian), como si optamos por un sistema operativo sobre el que vamos a instalar el lenguaje. Estas dos opciones serán las básicas a comparar, y en cualquier caso se tendrá que entender cómo está definido el contenedor base y qué proporciona: variables de entorno, usuarios, y programas auxiliares. Tendrás que tomar esta decisión para cada uno de los tres contenedores, tanto el de la API, como el de logs, como el de la base de datos.
    Instalación de paquetes adicionales que podamos necesitar. Por ejemplo: ¿necesitaré git? ¿Un compilador de C? ¿Una herramienta para descargar de la web?
    Instalación de las bibliotecas que necesite la aplicación.
    Cualquier otra cosa que se necesite para ejecutar la aplicación.

Entrega de la práctica

Subir los fuentes a GitHub mediante un pull request al fichero correspondiente en el repositorio de la asignatura. Como siempre, toda rúbrica tiene que estar correctamente identificada y enlazada desde el README, que, como en todos los hitos, reflejará el estado del proyecto del estudiante en este punto. El Dockerfile del estudiante tendrá que estar en el repositorio del proyecto. Aparte, se tendrá que publicar el contenedor en GitHub Container Registry con el mismo nombre que el proyecto (En GitHub Container Registry es donde se puede descargar el contenedor para ejecutarlo en otra máquina, no es el entorno desde el que se ejecuta en GitHub). Este repositorio estará configurado para que se construya el contenedor automáticamente cada vez que se actualice el repositorio en GitHub (GitHub actions para primero testear los contenedores y, al pasar los tests de los contenedores (que serán los mismos tests de la API pero sobre el contenedor, que ahora contedrá la API desplegada), publicar los contenedores automáticamente en GitHub Container Registry). El fichero compose.yaml debe estar en el directorio principal del proyecto. Habrá que añadir un test que construya el clúster y responda a algunas peticiones.
Valoración

    1,5 puntos: documentación y justificación de la estructura del clúster. Qué clúster de contenedores vas a usar (el de la API Python, el de la base de datos (MongoDB) y el de los logs)
    1,5 puntos: documentación y justificación de la configuración de cada uno de los contenedores que lo componen (el clúster).
    2 puntos: documentación del Dockerfile del contenedor para la aplicación.
    1,5 puntos: contenedor subido correctamente a GitHub Container Registry y documentación de la actualización automática.
    2 puntos: documentación del fichero de composición (compose.yml).
    1,5 puntos: testeo del cúster.
    Falta justificación de qué contenedores usarás y por qué, eso al principio del todo.

Esencialmente, es meter la API en un contenedor, más un contenedor de logs y otro de base de datos.

Añadir un sistema de inicio de sesión con roles de usuario. Implementa los roles de usuario ahora. Tienen que estar antes del hito 5. Implementamos un sistema de gestión de usuarios. En la nube, que solo los usuarios autorizados puedan acceder a la aplicación es fundamental. La aplicación original permite guardar flujos de trabajo en ficheros json, así como cargarlos desde ellos, pero ahora creamos dos roles de usuario, uno básico y otro premium. La idea es simular que el usuario premium es toda persona que pague por disponer de las funcionalidades de la aplicación que permiten guardar y cargar flujos de trabajo GeneSys usando ficheros .json. No sé cómo se inicia sesión si no hay interfaz gráfica.

Kibala para el contenedor de logs. Lo recomienda Claudia. El año anterior también usaron Astana.
