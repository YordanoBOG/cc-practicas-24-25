Hito 5: Despliegue de la aplicación en un PaaS

Escoger el PaaS gratuito que quieras y úsalo para desplegar. A veces hace falta un IaaS por debajo para desplegarlo. El PaaS debe estar desplegado en Europa y poder ser desplegado directamente desde GitHub por línea de comandos. ¿Se despliega el clúster de contenedores?

Descripción

Hacer un despliegue en la nube, usando una Plataforma como Servicio (PaaS), del proyecto de prácticas desarrollado.
Explicación

Necesito desplegar una aplicación contenerizada en un PaaS. El PaaS en el que desplegar la aplicación debe cumplir los siguientes requisitos:
1) El despliegue de la aplicación debe estar en Europa y ser accesible a través de una URL.
2) El servicio PaaS elegido debe ser gratuito o tener un periodo de prueba gratuito superior a un mes.
3) La configuración del despliegue debe definirse en un fichero que describa la infraestructura. Se puede hacer o bien con un lenguaje de configuración que provea el PaaS elegido, o bien mediante una secuencia de comandos de la herramienta de línea de órdenes que proporcione el PaaS.
4) El PaaS debe desplegarse desde el repositorio de GitHub en el que se encuentra la aplicación, de manera que el despliegue se produzca automáticamente con cada push que se haga al repositorio.
¿Qué servicio PaaS me recomiendas que cumpla estos requisitos?

El principal objetivo de este hito es familiarizarse con las técnicas usadas para desplegar aplicaciones desde un repositorio web a una Plataforma como Servicio (PaaS).

Para ello debe darse de alta en algún servicio PaaS disponible o usar alguno de los PaaS de otros servicios cloud en los que ya se esté dado de alta. Si lo prefiere puede desplegar su propio PaaS en algún IaaS disponible (por ejemplo, OpenStack).

Se plantea como objetivo el saber seleccionar el PaaS gratuito (o de pago pero gratuito durante un tiempo o para un nivel determinado servicio) más adecuado para las necesidades de la aplicación que se va a desplegar. El PaaS seleccionado tiene que cumplir tres requisitos:

    A efectos de evaluación, la configuración debe definirse en un fichero que describa la infraestructura. Se puede hacer o bien usando algún lenguaje o fichero de configuración que provea el PaaS, o bien mediante una secuencia de comandos introducidos a través de la herramienta de línea de órdenes (toolbelt) proporcionada por el PaaS. En ambos casos se tendrá que especificar claramente en la documentación de proyecto los pasos seguidos. El objetivo de esta parte es que una persona que se dé de alta y esté autorizada a usar ese PaaS pueda, usando ese fichero de configuración o secuencia de comandos, reproducir la infraestructura y desplegar el mismo proyecto. Si el PaaS sólo permite configuración desde la web, no sería válido.
    El PaaS debe permitir el despliegue directo desde el repositorio de GitHub. Es decir, que se pueda desde GitHub hacer el despliegue simplemente haciendo push desde el repositorio. La configuración de este despliegue se tendrá que documentar en README del repositorio de prácticas.
    Permitir el despliegue de la aplicación en Europa (legalmente obligatorio).

Debe abrir una cuenta en el proveedor de PaaS, crear la aplicación en la nube y ponerla en marcha. La herramienta que se use en el PaaS para lanzar la aplicación tendrá que hacer uso de las órdenes que se hayan utilizado en los hitos anteriores. De esta forma se asegura que se ejecuta de la misma forma como se hacía localmente.
Material adicional

    Apuntes de cursos anteriores sobre Despliegue de aplicaciones en la nube

Entrega de la práctica

Subir los fuentes a GitHub y hacer un pull request al fichero correspondiente en el repositorio de la asignatura.

Todos los elementos que se describen la rúbrica de valoración del hito tienen que estar correctamente identificados y enlazados desde el README, que reflejará el estado final del proyecto del estudiante.

Se tendrá que incluir la URL donde se haya desplegado la aplicación en el PaaS.
Valoración

    2 puntos: Descripción y justificación de los criterios usados para elegir el PaaS y las diferentes opciones valoradas. En el caso que haya sido necesario seleccionar un IaaS, justifique también su decisión.
    2 puntos: Descripción y justificación de las herramientas usadas para desplegar la aplicación en el PaaS.
    2 puntos: Descripción de la configuración para el despliegue automático al PaaS desde el repositorio de Github.
    3 puntos: Funcionamiento correcto del despliegue en el PaaS (no sólo el status, sino que correcto funcionamiento de la aplicación).
    1 punto: Pruebas de las prestaciones de la aplicación desplegada en el PaaS.
