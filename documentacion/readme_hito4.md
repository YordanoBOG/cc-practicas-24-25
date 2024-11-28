Añadir un sistema de logs (sistema de inicio de sesión con roles de usuario). Implementa los roles de usuario ahora. Tienen que estar antes del hito 5.

Si no me equivoco, ahora debes desplegar la base de datos.
    
Kibala para el contenedor de logs. Lo recomienda Claudia. El año anterior también usaron Astana. Esto es porque en el hito 4 se usarán contenedores.

-> Implementamos un sistema de gestión de usuarios. En la nube, que solo los usuarios autorizados puedan acceder a la aplicación es fundamental. Modificamos la pestaña inicial de la aplicación para incluir un sistema de autenticación de usuarios. La aplicación original permite guardar flujos de trabajo en ficheros json, así como cargarlos desde ellos. Creamos dos roles de usuario, uno básico y otro premium. La idea es simular que el usuario premium es toda persona que pague por disponer de las funcionalidades de la aplicación que permiten guardar y cargar flujos de trabajo GeneSys usando ficheros .json.

-> En hitos posteriores, cuando despleguemos una base de datos en un contenedor, los usuarios y sus contraseñas se almacenarán en ella. De momento, contamos con un usuario básico y otro premium (más sus contraseñas) de prueba en un fichero .json.