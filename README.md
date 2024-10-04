# CC-Practicas-24-25
Cloud Computing subject project.

En cada hito el fichero README.md describirá el estado del proyecto actual, y se sacará a otros ficheros (enlazándolos) la documentación adicional que haya podido necesitarse para la corrección de otros hitos. Subir los ficheros actualizados a GitHub y hacer un pull request para cada hito completado. Respecto a la documentación sobre la realización de este proyecto, conviene que se cree un documento aparte usando los diferentes mecanismos que ofrece GitHub y se enlace desde el fichero donde se explique el proyecto, en el directorio principal. O sea, incluir en este readme los enlaces a la documentación. La documentación se incluirá en ficheros Markdown.

--------------------------------------------------------------------------------
HITO 1

El presente proyecto de cloud computing pretende desplegar en la nube la aplicación diseñada en mi trabajo fin de grado (https://github.com/YordanoBOG/GeneSys). La aplicación en cuestión se llama GeneSys y permite preprocesar datos proteicos descargados de la base de datos genómica del Bacterial and Viral Bioinformatics Resource Center (https://www.bv-brc.org/) a través de un flujo personalizado por el usuario. La aplicación está diseñada casi en su totalidad en Python, con Kivy para la interfaz de usuario. Al ser una herramienta de procesado de datos, su despliegue en la nube tiene sentido, ya que habilitaría que los usuarios puedan procesar un mayor volumen de datos del que podrían estando limitados por la potencia de sus equipos de trabajo personales.

El problema que pretende resolver esta aplicación es uno de los pasos que se llevaron a cabo para realizar la siguiente publicación: https://academic.oup.com/nar/article/48/22/12632/6020195?login=false, donde se lleva a cabo un análisis de proteínas vecinas a partir de unas muestras previamente preprocesadas. GeneSys permite automatizar dicho preprocesado de los datos empleados en el estudio para que así se pueda repetir el experimento con más facilidad y empleando nuevas proteínas como objeto de estudio.

En concreto, las funcionalidades que tiene la aplicación son las siguientes:
-> Definir un flujo de trabajo al que se le pueden añadir hasta 5 tareas que se corresponden con los pasos a aplicar para realizar el preprocesamiento. Las tareas son:
   1) Aislar IDs de proteínas descargadas de la base de datos.
   2) Obtener las cadenas de proteínas a partir de los IDs.
   3) Reducir la muestra de proteínas para que solo haya un ejemplar de cada familia evolutiva (tener una muestra de una rama evolutiva que ya está representada se considera ruido, y debe eliminarse).
   4) Obtener 30000 nucleótidos vecinos previos y posteriores a cada proteína aislada en el paso anterior, que a partir de ahora serán consideradas cebos.
   5) Revisar las cadenas de nucleótidos en busca de codones de parada (un codón de parada válido equivale a una proteína vecina asociada a la proteína cebo que la contiene). Organizar los resultados obtenidos y devolverlos en un archivo xlsx.
-> Eliminar tareas del flujo de trabajo.
-> Guardar el flujo actual en un archivo .json.
-> Cargar un flujo desde un archivo .json.
-> Ejecutar el flujo.
-> Cancelar la ejecución del flujo.

De momento, se han añadido los ficheros de la aplicación al repositorio de GitHub, y se ha aprovechado para resolver una falla de diseño que la aplicación traía de base, que consistía en almacenar como atributo de la interfaz de usuario un dato que realmente iba asociado al flujo de trabajo.

--------------------------------------------------------------------------------
HITO 2

Modificamos la aplicación del TFG para transformarla en una aplicación que pueda aprovechar todas las ventajas de la nube. Realizamos las siguientes modificaciones sobre el código original:

-> Reducimos la funcionalidad de la aplicación para que la arquitectura sea más sencilla. Originalmente, GeneSys estaba orientada a poseer una gran extensibilidad. Simplificamos el código para que sea menos complejo a costa de reducir la extensibilidad, ya que en la asignatura de CC nos vamos a centrar en emplear las funciones que GeneSys ofrece, no a incorporar otras nuevas.

-> Implementamos un sistema de gestión de usuarios. En la nube, que solo los usuarios autorizados puedan acceder a la aplicación es fundamental. Modificamos la pestaña inicial de la aplicación para incluir un sistema de autenticación de usuarios. La aplicación original permite guardar flujos de trabajo en ficheros json, así como cargarlos desde ellos. Creamos dos roles de usuario, uno básico y otro premium. La idea es simular que el usuario premium es toda persona que pague por disponer de las funcionalidades de la aplicación que permiten guardar y cargar flujos de trabajo GeneSys usando ficheros .json.

-> En hitos posteriores, cuando despleguemos una base de datos en un contenedor, los usuarios y sus contraseñas se almacenarán en ella. De momento, contamos con un usuario básico y otro premium (más sus contraseñas) de prueba en un fichero .json.

--------------------------------------------------------------------------------
HITO 3
