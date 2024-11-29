Hito 3: Diseño de microservicios

En este hito vamos a crear un microservicio sobre la base de la funcionalidad desarrollada en el hito anterior. Para ello, nos serviremos de la biblioteca Flask de Python, que permite definir endpoints para APIs de una forma sencilla y rápida, perfecta para un principiante como yo. Uniremos Flask con las herramientas aprendidas en el hito 2 (Automatización de pruebas con un archivo .yml, pytest y GitHub actions). Por tanto, usaremos el entorno de GitHub actions para desplegar una API hecha con la biblioteca Flask de Python sobre la que realizaremos tests, todo orquestrado a través de un archivo .yml.

Comenzamos definiendo nuestra API incorporando un archivo "app/api.py" que incluye los endpoints para acceder a la funcionalidad de nuestra API: únicamente habilitamos las funcionalidades que nos interesa ofrecer al usuario. Dichos endpoints incluyen mensajes de log que informan por pantalla cada vez que se produce una llamada a cualquiera de ellos.

Las funciones de nuestra API van a ir ligadas al manejo de flujos de trabajo para datos genéticos, en concreto, se podrá 

\capturas de api.py

Por temas de organización, definimos la aplicación en un archivo __init__.py situado en la misma ruta "app/__init__.py". En dicho archivo se define la aplicación Flask que hemos implementado, y se importan todas las funcionalidades disponibles a través de la API

\captura de init

Junto a eso, eliminamos el archivo "main.py" que originalmente lanzaba la aplicación, y en su lugar creamos un archivo "app.py" en el fichero raíz, que pone a punto la API para recibir solicitudes.

\captura de app.py

Para testear la API, creamos un nuevo fichero de test en "tests/test_api.py", que se encargará de evaluar los endpoints del servicio.

\capturas de test_api.py

Finalmente, para automatizar el despliegue y testeo de la API con cada push que se haga a la rama main del repositorio, añadimos una nueva tarea al archivo ".github/workflow/genesys_tests.yml" del hito anterior, que se encargará de lanzar el script Python que pone en marcha la API junto al archivo que ejecuta los tests sobre ella.

\captura de la nueva sección de genesys_tests.yml

Si hacemos un push en nuestro repositorio GitHub, podremos ver que se ejecutan tanto los tests del hito 2 como los de la API del hito 3.

\Capturas

-------------------------------------------------------------------------------

Diseñar una API consistente en una serie de rutas (en el caso de un API REST), testear la API usando una biblioteca específica que te provea el microservicio y crear la infraestructura necesaria para comenzar a ejecutarlo.

La valoración se distribuirá en las siguientes rúbricas:

    2 puntos: Justificación técnica del framework elegido para el microservicio. Entorno empleado para implementar el microservicio.
    4 puntos: Diseño en general de la API, las rutas (o tareas), tests y documentación de todo, de forma que reflejen correctamente un diseño por capas que desacopla la lógica de negocio de la API.
    2 puntos: Uso de logs para registrar la actividad de la API, incluyendo la justificación del framework y herramienta elegida. Los logs permiten revisar qué hace la persona que accede a la API.
    2 puntos: Correcta ejecución de los tests. (De los tests de la API, porque los del hito 2 supuestamente ya los tienes).
