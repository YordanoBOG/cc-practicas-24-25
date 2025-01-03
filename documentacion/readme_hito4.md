Hito 4: Composición de servicios

En el hito 4 hemos conteneirizado la aplicación de GeneSys para poder manipular la API a través de endpoints desplegados en un contenedor que además interactúan con una base de datos mongo. Hemos realizado una serie de modificaciones iniciales sobre el código de la aplicación original:

-> Eliminamos la interfaz de usuario en Kivy, ya que no es necesaria para interactuar con la API.
-> Eliminamos las dos últimas tareas de las cinco de las que disponíamos inicialmente para la app, ya que el volumen de trabajo se agrandaba demasiado en caso de mantenerlas. Además, la cuarta tarea trabajaba con el shell de Linux para generar archivos locales, y no ha dado tiempo a adaptar esa funcionalidad para manipular archivos en la base de datos.

Definimos el siguiente docker-compose:

captura

Con el siguiente Dockerfile para la app:

captura

Dado que inicialmente trabajábamos con archivos en la ruta local, ahora disponemos de una variable especial que indica si debemos conectarnos o no a la base de datos para manipular los archivos:

captura

Esta variable define si la app debe trabajar con la ruta local o con la base de datos, según si se ejecuta en un entorno u otro. Esto se hace así para que los tests de las anteriores prácticas se sigan evaluando de forma satisfactoria.

Definimos el siguiente archivo yaml para publicar los contenedores en GitHub container registry:

captura

El archivo ejecuta los siguientes tests sobre los endpoints de la API usando la orden curl:

captura

Si se accede a app.py, se pueden observar ejemplos comentados de interacción con cada uno de los endpoints disponibles de la aplicación a través de la orden curl:

captura
