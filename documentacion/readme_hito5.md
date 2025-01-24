Hito 5: Despliegue de la aplicación en un PaaS. Documentación.

Vamos a relatar el despliegue en servidores europeos de nuestra aplicación contenerizada usando un formato de descripción de la arquitectura en formato código que, además, está vinculado a nuestro repositorio de GitHub y se redespliega con cada push que se hace en él.

El PaaS que vamos a usar es Render, porque ofrece una versión gratuita adecuada para probar nuestra aplicación y, si se vincula un despliegue con una rama determinada de un repositorio de GitHub, realiza redespliegues automáticos cada vez que se realiza un push sobre dicha rama. Otras opciones que se valoraron en un inicio fueron Fly.io y Railway.app. Ambas ofrecen soporte para vincular el despliegue con GitHub, así como el uso de un fichero para describir la infraestructura del despliegue en formato como código. No obstante, Fly.io se descartó por no poseer despliegues automáticos con cada push, y Railway.app era mucho más restrictivo para el despliegue de clusters de contenedores, ya que obligaba a desplegar el servicio especificando un dockerfile, mientras que Render admite despliegues de múltiples imágenes especificando distintos dockerfiles.

Entramos en la página oficial de Render y, tras crear una cuenta vinculando GitHub, damos acceso a nuestros repositorios. Ahora podemos crear servicios desplegados sobre el repositorio que seleccionemos.

Para desplegar un nuevo servicio, debe seleccionarse New -> Web Service. Sin embargo, esta opción permite desplegar un servicio usando la interfaz web, que no es lo que nos interesa. En su lugar, usamos la opción New -> Blueprint, que es el mecanismo para desplegar una nueva infraestructura en formato como código.




Necesito desplegar una aplicación contenerizada en un PaaS. El PaaS en el que desplegar la aplicación debe cumplir los siguientes requisitos:
1) El despliegue de la aplicación debe estar en Europa y ser accesible a través de una URL.
2) El servicio PaaS elegido debe ser gratuito o tener un periodo de prueba gratuito superior a un mes.
3) La configuración del despliegue debe definirse en un fichero que describa la infraestructura. Se puede hacer o bien con un lenguaje de configuración que provea el PaaS elegido, o bien mediante una secuencia de comandos de la herramienta de línea de órdenes que proporcione el PaaS.
4) El PaaS debe desplegarse desde el repositorio de GitHub en el que se encuentra la aplicación, de manera que el despliegue se produzca automáticamente con cada push que se haga al repositorio.
¿Qué servicio PaaS me recomiendas que cumpla estos requisitos?

Entrega de la práctica

Se tendrá que incluir la URL donde se haya desplegado la aplicación en el PaaS.
Valoración

    2 puntos: Descripción y justificación de los criterios usados para elegir el PaaS y las diferentes opciones valoradas. En el caso que haya sido necesario seleccionar un IaaS, justifique también su decisión.
    2 puntos: Descripción y justificación de las herramientas usadas para desplegar la aplicación en el PaaS.
    2 puntos: Descripción de la configuración para el despliegue automático al PaaS desde el repositorio de Github.
    3 puntos: Funcionamiento correcto del despliegue en el PaaS (no sólo el status, sino que correcto funcionamiento de la aplicación).
    1 punto: Pruebas de las prestaciones de la aplicación desplegada en el PaaS.
