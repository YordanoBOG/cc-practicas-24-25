Hito 3: Diseño de microservicios

En este hito vamos a crear un microservicio sobre la base de la funcionalidad desarrollada en el hito anterior.

Comenzamos definiendo nuestra API incorporando un archivo "app/api.py" que incluye los endpoints para acceder a la funcionalidad de nuestra apicación.

\captura de api.py

Junto a eso, eliminamos el archivo main.py que originalmente lanzaba la aplicación, y en su lugar creamos el archivo app.py en el fichero raíz, que pone a punto la API para recibir solicitudes.

\captura de app.py

Para testear la API, creamos un nuevo fichero de test en tests/test_api.py, que se encargará de evaluar los endpoints del servicio.

\captura de test_api.py

Finalmente, para automatizar el despliegue y testeo de la API con cada push que se haga a la rama main del repositorio, añadimos una nueva tarea al archivo .github/workflow/genesys_tests.yml del hito anterior, que se encargará de lanzar el script Python que pone en marcha la API, junto al archivo que ejecuta los tests sobre ella.

\captura de la nueva sección de genesys_tests.yml

-------------------------------------------------------------------------------

Diseñar una API consistente en una serie de rutas (en el caso de un API REST), testear la API usando una biblioteca específica que te provea el microservicio y crear la infraestructura necesaria para comenzar a ejecutarlo.

No hagas los tests con postman/swagger o algo de eso, sino a partir del yaml.

Dale al usuario solo la funcionalidad que te interesa proporcionar a través de APIs.

Entrega de la práctica

En este punto, el código que se haya entregado tiene que estar en el siguiente estado:

    Debe incluir, al menos, un servicio de configuración que considere las diferentes posibilidades.
    Debe tener la estructura general de las clases que se vayan a servir con la API correcta, incluyendo en su caso diseño de excepciones que puedan ocurrir en el curso normal de ejecución de la aplicación.
    No deben incluir ningún tipo de acceso a datos, pero si lo hacen debe hacerse a través de una single source of truth usando inyección de dependencias. El test de la misma se debe hacer de la misma forma.
    No es necesario, ni se solicita, que haya una "aplicación" lanzable y se prefiere que no la haya. El código debe ser única y exclusivametne el necesario para testear las rutas, y es conveniente que, en el diseño por capas, se separe la lógica de negocio de la lógica del API y esta, a su vez, del programa o aplicación desde las que se van a usar ambos.
    En este punto la aplicación puede estar potencialmente en Internet. La comprobación de tipos debe ser exhaustiva, tanto la que provea el sistema de tipos del lenguaje como la que se haga por parte del usuario en caso de que no sea así.

La valoración se distribuirá en las siguientes rúbricas:

    2 puntos: Justificación técnica del framework elegido para el microservicio. Entorno empleado para implementar el microservicio.
    4 puntos: Diseño en general de la API, las rutas (o tareas), tests y documentación de todo, de forma que reflejen correctamente un diseño por capas que desacopla la lógica de negocio de la API.
    2 puntos: Uso de logs para registrar la actividad de la API, incluyendo la justificación del framework y herramienta elegida. Los logs permiten revisar qué hace la persona que accede a la API.
    2 puntos: Correcta ejecución de los tests. (De los tests de la API, porque los del hito 2 supuestamente ya los tienes).
