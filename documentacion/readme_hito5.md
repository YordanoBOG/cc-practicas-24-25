Hito 5: Despliegue de la aplicación en un PaaS. Documentación.

Vamos a relatar el despliegue en servidores europeos de nuestra aplicación contenerizada usando un formato de descripción de la arquitectura en formato código que, además, está vinculado a nuestro repositorio de GitHub y se redespliega con cada push que se hace en él.

El PaaS que vamos a usar es Render, porque ofrece una versión gratuita adecuada para probar nuestra aplicación y, si se vincula un despliegue con una rama determinada de un repositorio de GitHub, realiza redespliegues automáticos cada vez que se realiza un push sobre dicha rama. Otras opciones que se valoraron en un inicio fueron Fly.io y Railway.app. Ambas ofrecen soporte para vincular el despliegue con GitHub, así como el uso de un fichero para describir la infraestructura del despliegue en formato como código. No obstante, Fly.io se descartó por no poseer despliegues automáticos con cada push, y Railway.app era mucho más restrictivo para el despliegue de clusters de contenedores, ya que obligaba a desplegar el servicio especificando un dockerfile, mientras que Render admite despliegues de múltiples imágenes especificando distintos dockerfiles.

Entramos en la página oficial de Render y, tras crear una cuenta vinculando GitHub, damos acceso a nuestros repositorios. Ahora podemos crear servicios desplegados sobre el repositorio que seleccionemos.

Para desplegar un nuevo servicio, debe seleccionarse New -> Web Service. Sin embargo, esta opción permite desplegar un servicio usando la interfaz web, que no es lo que nos interesa. En su lugar, usamos la opción New -> Blueprint, que es el mecanismo para desplegar una nueva infraestructura en formato como código.

De primeras especificamos las opciones del servicio manualmente a través de la web, elegimos el repositorio de GitHub de los hitos de CC.

Y elegimos las opciones genéricas del servicio, entre las que caben destacar plan: free (para usar el servicio PaaS gratuito), region: frankfurt (despliegue en Europa) y autodeploy: true (para que se relance el servicio con cada push al repositorio).

Una vez tenemos el servicio creado, cada vez que se lance buscará un fichero llamado "render.yaml" en la raíz del repositorio de GitHub, que contendrá la especificación de la infraestructura a desplegar, y lo usará como archivo de configuración del servicio. Si no encuentra el fichero o si está mal configurado, fallará.

Nuestro fichero de configuración de GitHub, de primeras, se encuentra configurado para desplegar la aplicación descrita en el Dockerfile, sin la base de datos Mongo.

En concreto, el fichero describe

Tras realizar un push, Render detecta el archivo render.yaml automáticamente e inicia el despliegue.

Dado que nuestra aplicación carece de interfaz, debemos fijarnos en las estructuras de datos devueltas al llamar a la API. Con una orden curl desde el terminal de Ubuntu podemos verificar que la app se encuentra desplegada y que funciona, por ejemplo, creando un nuevo flujo de trabajo.

Otros endpoints que trabajan con la base de datos (como el endpoint que consulta la base de datos) se quedan colgados, ya que la app no es capaz de encontrar la conexión a la base de datos Mongo.

No obstante, de momento hemos conseguido desplegar la aplicación en un PaaS cumpliendo los requisitos solicitados en el hito 5: el despliegue está en Europa, es accesible a través de una URL, el servicio PaaS elegido es gratuito, la configuración del despliegue está definida en un fichero que describe la infraestructura, y el despliegue está sincronizado con GitHub para realizarse automáticamente con cada push.

Ahora tenemos que comunicar la aplicación con una base de datos. Dado que nuestra app trabaja con documentos, necesitamos emplear una base de datos no relacional (en concreto, Mongo). Render permite desplegar un servicio de base de datos Postgre que, de forma gratuita, puede conectarse con la aplicación, pero Postgre es un sistema gestor de bases de datos relacional, por lo que no nos sirve.

Necesitamos desplegar un servicio Mongo

Entrega de la práctica

Se tendrá que incluir la URL donde se haya desplegado la aplicación en el PaaS.
Valoración

    2 puntos: Descripción y justificación de los criterios usados para elegir el PaaS y las diferentes opciones valoradas. En el caso que haya sido necesario seleccionar un IaaS, justifique también su decisión.
    2 puntos: Descripción y justificación de las herramientas usadas para desplegar la aplicación en el PaaS.
    2 puntos: Descripción de la configuración para el despliegue automático al PaaS desde el repositorio de Github.
    3 puntos: Funcionamiento correcto del despliegue en el PaaS (no sólo el status, sino que correcto funcionamiento de la aplicación).
    1 punto: Pruebas de las prestaciones de la aplicación desplegada en el PaaS.
