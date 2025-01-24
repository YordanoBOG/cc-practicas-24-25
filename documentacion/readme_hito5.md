Hito 5: Despliegue de la aplicación en un PaaS. Documentación.

Vamos a relatar el despliegue en servidores europeos de nuestra aplicación contenerizada usando un formato de descripción de la arquitectura en formato código que, además, está vinculado a nuestro repositorio de GitHub y se relanza en el PaaS con cada push.

El PaaS que vamos a usar es Render, porque ofrece una versión gratuita adecuada para probar nuestra aplicación y, si se vincula un despliegue con una rama determinada de un repositorio de GitHub, realiza redespliegues automáticos cada vez que se realiza un push sobre dicha rama. Otras opciones que se valoraron en un inicio fueron Fly.io y Railway.app. Ambas ofrecen soporte para vincular el despliegue con GitHub, así como el uso de un fichero para describir la infraestructura del despliegue en formato como código. No obstante, Fly.io se descartó por no poseer despliegues automáticos con cada push, y Railway.app era mucho más restrictivo para el despliegue de clusters de contenedores, ya que obligaba a desplegar el servicio especificando un dockerfile, mientras que Render admite despliegues de múltiples imágenes especificando distintos dockerfiles (https://alexfranz.com/posts/deploying-container-apps-2024/).

Entramos en la página oficial de Render y, tras crear una cuenta vinculando GitHub, damos acceso a nuestros repositorios. Ahora podemos crear servicios desplegados sobre el repositorio que seleccionemos.

![Captura desde 2025-01-24 08-35-15](https://github.com/user-attachments/assets/0d022971-133e-4c55-be7b-e97f9f0098dd)

Antes de desplegar el servicio, creamos un proyecto (project) en Render específico de las prácticas de la asignatura. Esto nos permite alojar todos los servicios que vamos a emplear para un mismo objetivo en un único lugar, y ayuda a estructurar nuestros despliegues de Render en general.

![Captura desde 2025-01-24 10-44-28](https://github.com/user-attachments/assets/104a4423-969c-424b-ba12-cd31d69f1766)

Para desplegar un nuevo servicio, debe seleccionarse New -> Web Service. Sin embargo, esta opción sirve para desplegar un servicio usando la interfaz web, que no es lo que nos piden hacer. En su lugar, usamos la opción New -> Blueprint, que es el mecanismo para desplegar una infraestructura en formato código.

![Captura desde 2025-01-24 08-36-28](https://github.com/user-attachments/assets/7cab1b54-c57e-4e37-8ab6-77947ad911c6)

De primeras especificamos las opciones del servicio manualmente a través de la web, elegimos el repositorio de GitHub de los hitos de CC (cc-practicas-24-25).

![Captura desde 2025-01-23 18-16-09](https://github.com/user-attachments/assets/bea8908d-7346-46c5-8a54-e56ff70f357e)

Y seleccionamos las opciones genéricas del servicio, entre las que caben destacar plan: free (para usar el servicio PaaS gratuito), region: frankfurt (despliegue en Europa), branch: main (indicando que se debe desplegar el servicio usando el contenido de la rama main) y autodeploy: true (para que se relance el servicio con cada push al repositorio).

![Captura desde 2025-01-23 18-16-53](https://github.com/user-attachments/assets/2966b67f-cb28-46da-a63e-614703659878)

Una vez tenemos el servicio creado, cada vez que se lance buscará un fichero llamado "render.yaml" en la rama main de nuestro repositorio de GitHub, que contendrá la especificación de la infraestructura a desplegar, y lo usará como archivo de configuración del servicio. Si no encuentra el fichero o si está mal configurado, fallará.

![Captura desde 2025-01-23 18-17-11](https://github.com/user-attachments/assets/fc9376dc-7cb0-4a6d-bf49-ad388ca32ffd)

El fichero de configuración "render.yaml", de primeras, se encuentra configurado para desplegar la aplicación descrita en el Dockerfile, sin la base de datos Mongo.

![Captura desde 2025-01-24 10-34-35](https://github.com/user-attachments/assets/f9fe72ad-6564-44a3-9f72-017ece8860ac)

En concreto, el fichero describe un servicio web llamado "genesys_api", se especifica el repositorio GitHub a partir del que realizar el despligue, la ruta al Dockerfile, las opciones especificadas previamente en el despliegue manual y un par de variables de entorno que especifican el servicio PaaS en el que se despliega la app y el puerto de escucha (ambas variables son opcionales, pues la primera es meramente informativa y la segunda ya va especificada en el Dockerfile).

Tras realizar un push sobre la rama main, Render detecta el archivo render.yaml automáticamente e inicia el despliegue. Si entramos en el servicio, observamos que existe un despliegue por cada push que hemos realizado, donde el más reciente es el primero que aparece en la lista (en la captura de abajo se pude observar que ya hemos realizado múltiples despliegues, y que el último de ellos ha sido exitoso).

![Captura desde 2025-01-24 10-46-05](https://github.com/user-attachments/assets/58fe6c55-8435-4132-aa0e-e6000552eb75)

Si clicamos en el último despliegue, podemos ver la ventana de logs.

![Captura desde 2025-01-24 10-53-58](https://github.com/user-attachments/assets/9bb713d8-1794-4fa1-8965-9c7bd0335dd2)

La URL de despliegue de la aplicación es https://genesys-api.onrender.com/. Dado que nuestra aplicación carece de interfaz, debemos fijarnos en las estructuras de datos devueltas al llamar a la API. Con una orden curl desde el terminal de Ubuntu podemos verificar que la app se encuentra desplegada y que funciona, por ejemplo, creando un nuevo flujo de trabajo.

![Captura desde 2025-01-24 10-54-47](https://github.com/user-attachments/assets/c603c5d2-bb98-4a6c-a387-f54f2794c673)

Otros endpoints que trabajan con la base de datos (como el endpoint que consulta la base de datos) se quedan colgados, ya que la app no es capaz de encontrar la conexión a la base de datos Mongo.

![Captura desde 2025-01-24 10-54-58](https://github.com/user-attachments/assets/142a6488-7c43-4d59-8e29-643f1f906472)

No obstante, de momento hemos conseguido desplegar la aplicación en un PaaS cumpliendo los requisitos solicitados en el hito 5: el despliegue está en Europa, es accesible a través de una URL, el servicio PaaS elegido es gratuito, la configuración está en un fichero que describe la infraestructura, y el despliegue está sincronizado con GitHub para realizarse automáticamente con cada push.

Ahora tenemos que comunicar la aplicación con una base de datos. Dado que nuestra app trabaja con documentos, necesitamos emplear una base de datos no relacional (en concreto, Mongo). Render permite desplegar un servicio de base de datos Postgre que, de forma gratuita, puede conectarse con la aplicación, pero Postgre es un sistema gestor de bases de datos relacional, por lo que no nos sirve.

![Captura desde 2025-01-24 10-57-36](https://github.com/user-attachments/assets/abb773a2-6b2b-4476-8409-fb0da4c21839)

Necesitamos desplegar un servicio Mongo. Para ello, intentamos varias soluciones. La primera es intentar definir una configuración de varios servicios en el fichero "render.yaml". Inclumos dos nuevos servicios para la base de datos mongo y para el servicio de logging.

Entrega de la práctica

Se tendrá que incluir la URL donde se haya desplegado la aplicación en el PaaS.

    2 puntos: Descripción y justificación de las herramientas usadas para desplegar la aplicación en el PaaS.
    2 puntos: Descripción de la configuración para el despliegue automático al PaaS desde el repositorio de Github.
    3 puntos: Funcionamiento correcto del despliegue en el PaaS (no sólo el status, sino que correcto funcionamiento de la aplicación).
    1 punto: Pruebas de las prestaciones de la aplicación desplegada en el PaaS.
