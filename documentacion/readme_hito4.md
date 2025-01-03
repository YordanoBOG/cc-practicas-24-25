Hito 4: Composición de servicios

En el hito 4 hemos conteneirizado la aplicación de GeneSys para poder manipular la API a través de endpoints desplegados en un contenedor que además interactúan con una base de datos mongo. Hemos realizado una serie de modificaciones iniciales sobre el código de la aplicación original:

-> Eliminamos la interfaz de usuario en Kivy, ya que no es necesaria para interactuar con la API.
-> Eliminamos las dos últimas tareas de las cinco de las que disponíamos inicialmente para la app, ya que el volumen de trabajo se agrandaba demasiado en caso de mantenerlas. Además, la cuarta tarea trabajaba con el shell de Linux para generar archivos locales, y no ha dado tiempo a adaptar esa funcionalidad para manipular archivos en la base de datos.

Definimos el siguiente docker-compose:

![Captura desde 2025-01-03 11-58-10](https://github.com/user-attachments/assets/a04b09d9-0a12-4440-9586-8622ac4b40c0)

Con el siguiente Dockerfile para la app:

![Captura desde 2025-01-03 11-58-18](https://github.com/user-attachments/assets/082ff4ae-d9e5-4069-9c6e-1ec96ce8e93a)

Dado que inicialmente trabajábamos con archivos en la ruta local, ahora disponemos de una variable especial que indica si debemos conectarnos o no a la base de datos para manipular los archivos:

![Captura desde 2025-01-03 11-59-26](https://github.com/user-attachments/assets/e32f6078-5168-48ff-a586-52572e2dbbce)

Esta variable define si la app debe trabajar con la ruta local o con la base de datos, según si se ejecuta en un entorno u otro. Esto se hace así para que los tests de las anteriores prácticas se sigan evaluando de forma satisfactoria.

Definimos el siguiente archivo yaml para publicar los contenedores en GitHub container registry:

![Captura desde 2025-01-03 12-00-11](https://github.com/user-attachments/assets/f9e8b18b-966c-45ce-aece-a08ac276f2ad)
![Captura desde 2025-01-03 12-00-16](https://github.com/user-attachments/assets/c804be18-410f-4ef1-91ff-38477698fef2)

El archivo ejecuta los siguientes tests sobre los endpoints de la API usando la orden curl:

![Captura desde 2025-01-03 12-00-30](https://github.com/user-attachments/assets/1893f38f-2ed3-49a9-becb-418141f3da6c)

Si se accede a app.py, se pueden observar ejemplos comentados de interacción con cada uno de los endpoints disponibles de la aplicación a través de la orden curl:
![Captura desde 2025-01-03 12-00-58](https://github.com/user-attachments/assets/9836e9c5-a917-4036-99a7-90400e85c250)
