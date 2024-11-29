Hito 3: Diseño de microservicios

En este hito vamos a crear un microservicio sobre la base de la funcionalidad desarrollada en el hito anterior. Para ello, nos serviremos de la biblioteca Flask de Python, que permite definir endpoints para APIs de una forma sencilla y rápida, perfecta para un principiante como yo. Uniremos Flask con las herramientas aprendidas en el hito 2 (Automatización de pruebas con un archivo .yml, pytest y GitHub actions). Por tanto, usaremos el entorno de GitHub actions para desplegar una API hecha con la biblioteca Flask de Python sobre la que realizaremos tests, todo orquestrado a través de un archivo .yml.

-------------------------------------------------------------------------------

Comenzamos definiendo nuestra API incorporando un archivo "app/api.py" que incluye los endpoints para acceder a la funcionalidad de nuestra API: únicamente habilitamos las funcionalidades que nos interesa ofrecer al usuario. Dichos endpoints incluyen mensajes de log que informan por pantalla cada vez que se produce una llamada a cualquiera de ellos.

Las funciones de nuestra API van a ir ligadas al manejo de flujos de trabajo para datos genéticos, en concreto, se podrá crear un flujo/workflow vacío:

![Captura desde 2024-11-29 06-10-14](https://github.com/user-attachments/assets/6dea7ed8-8a74-4b12-a444-b7b6d41b27ca)

Y un flujo con unos parámetros específicos:

![Captura desde 2024-11-29 06-10-50](https://github.com/user-attachments/assets/a63ac0a8-bd23-4c6b-af51-afc87c2d979d)

También habrá endpoints específicos para incluir cada una de las posibles tareas que se le pueden añadir al flujo:

![Captura desde 2024-11-29 06-11-08](https://github.com/user-attachments/assets/3d500638-08be-407f-9faf-8ae91f0bd77b)
![Captura desde 2024-11-29 06-11-22](https://github.com/user-attachments/assets/612c5e12-cb2f-453f-bb83-269d950145d9)
![Captura desde 2024-11-29 06-11-35](https://github.com/user-attachments/assets/635e0b87-83f5-4eae-bc45-19e1b975720b)

Se incluye la posibilidad tanto de eleiminar la última tarea al flujo como de eliminar todas las que tenga:

![Captura desde 2024-11-29 06-11-47](https://github.com/user-attachments/assets/dc4277ff-086b-4427-ac44-35c20acae4ad)

El flujo puede guardarse y cargarse en un archivo JSON almacenado en una ruta personalizada:

![Captura desde 2024-11-29 06-11-58](https://github.com/user-attachments/assets/a2d82dab-0d36-432b-b002-a40742d857ad)

Y por último, pero no menos importante, el flujo puede ejecutarse:

![Captura desde 2024-11-29 06-12-14](https://github.com/user-attachments/assets/87ae6c86-f4f1-4f3a-beaa-c357b516755b)

Para el diseño del tipo de solicitudes, se han decidido establecer como "GET" aquellas que no necesitan transmitir información a la API, y como "POST" las demás.

Por temas de organización, definimos la aplicación en un archivo __init__.py situado en la ruta "app/__init__.py". En dicho archivo se define la aplicación Flask que hemos implementado, y se importan todas las funcionalidades disponibles a través de la API

![Captura desde 2024-11-29 06-22-00](https://github.com/user-attachments/assets/ae2afb45-b8dd-4c44-89bb-d5eeba3d1cf0)

-------------------------------------------------------------------------------

Junto a eso, eliminamos el archivo "main.py" que originalmente lanzaba la aplicación, y en su lugar creamos un archivo "app.py" en el fichero raíz, que pone a punto la API para recibir solicitudes.

![Captura desde 2024-11-29 06-24-05](https://github.com/user-attachments/assets/c42d59ff-f64a-4b71-90de-bd3f78271283)

-------------------------------------------------------------------------------

Para testear la API, creamos un nuevo fichero de test en "tests/test_api.py", que se encargará de evaluar los endpoints del servicio ejecutando un total de 12 pruebas independientes.

Primero creamos un nuevo flujo dos veces, una con los parámetros por defecto y otra con los parámetros personalizados.

![Captura desde 2024-11-29 06-29-02](https://github.com/user-attachments/assets/fada7c4f-242b-47d6-b370-672f58cc74fc)

Después, añadimos las cinco tareas posibles al flujo.

![Captura desde 2024-11-29 06-30-14](https://github.com/user-attachments/assets/41fd8c13-2376-450b-a6ee-bb8f807fa2aa)

Guardamos el flujo en un archivo JSON, lo vaciamos de contenido, lo volvemos a cargar desde ese archivo y lo ejecutamos.

![Captura desde 2024-11-29 06-31-10](https://github.com/user-attachments/assets/803cb815-e6aa-46f0-9e0e-589ac56dab8a)

-------------------------------------------------------------------------------

Finalmente, para automatizar el despliegue y testeo de la API con cada push que se haga a la rama main del repositorio, añadimos una nueva tarea al archivo ".github/workflow/genesys_tests.yml" del hito anterior, que se encargará de lanzar el script Python que pone en marcha la API junto al archivo que ejecuta los tests sobre la API.

![Captura desde 2024-11-29 06-33-06](https://github.com/user-attachments/assets/070f960d-7ca9-4d9e-9858-225bb5310e99)

-------------------------------------------------------------------------------

En esta captura se puede apreciar la organización actual del repositorio, donde las carpetas se han organizado con vistas a desacoplar la lógica de negocio (contenida en los directorios "kv_files", "modules", "screens" y "utils") de la API (que se lanza con "app-py", se define en el directorio "app", y se testea a través del yml en ".github/workflows" y los ficheros del directorio "tests").

![Captura desde 2024-11-29 06-28-11](https://github.com/user-attachments/assets/e22238d1-3b63-4a2d-a217-a97f106a14e2)

-------------------------------------------------------------------------------

Si hacemos un push en nuestro repositorio GitHub, podremos ver que se ejecutan tanto los tests del hito 2 como los de la API del hito 3.

![Captura desde 2024-11-29 06-38-36](https://github.com/user-attachments/assets/e6340d77-f756-45f7-b296-7f0a1b0e1d9f)
![Captura desde 2024-11-29 06-39-51](https://github.com/user-attachments/assets/9227e1d4-5d31-4e92-be81-a0a99f7b562f)
![Captura desde 2024-11-29 06-40-02](https://github.com/user-attachments/assets/a0053261-f79c-45cb-996c-60976e550bec)
