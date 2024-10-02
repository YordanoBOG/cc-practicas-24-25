# CC-Practicas-24-25
Cloud Computing subject project.

En cada hito el fichero README.md describirá el estado del proyecto actual, y se sacará a otros ficheros (enlazándolos) la documentación adicional que haya podido necesitarse para la corrección de otros hitos. Subir los ficheros actualizados a GitHub y hacer un pull request para cada hito completado. Respecto a la documentación sobre la realización de este proyecto, conviene que se cree un documento aparte usando los diferentes mecanismos que ofrece GitHub y se enlace desde el fichero donde se explique el proyecto, en el directorio principal. O sea, incluir en este readme los enlaces a la documentación. La documentación se incluirá en ficheros Markdown.

--------------------------------------------------------------------------------
HITO 1

El presente proyecto de cloud computing pretende desplegar en la nube la aplicación diseñada en mi trabajo fin de grado (https://github.com/YordanoBOG/GeneSys). La aplicación en cuestión se llama GeneSys y permite preprocesar datos proteicos descargados de la base de datos genómica del Bacterial and Viral Bioinformatics Resource Center (https://www.bv-brc.org/) a través de un flujo personalizado por el usuario. La aplicación está diseñada casi en su totalidad en Python, con Kivy para la interfaz de usuario. Al ser una herramienta de procesado de datos, su despliegue en la nube tiene sentido, ya que habilitaría que los usuarios puedan procesar un mayor volumen de datos del que podrían estando limitados por la potencia de sus equipos de trabajo personales.

El problema que pretende resolver esta aplicación es uno de los pasos que se llevaron a cabo para realizar la siguiente publicación: https://academic.oup.com/nar/article/48/22/12632/6020195?login=false, donde se lleva a cabo un análisis de proteínas vecinas a partir de unas muestras previamente preprocesadas. GeneSys permite automatizar dicho preprocesado de los datos empleados en el estudio para que así se pueda repetir el experimento con más facilidad y empleando nuevas proteínas como objeto de estudio.

De momento, se han añadido los ficheros de la aplicación al repositorio de GitHub al tiempo que se ha aprovechado para resolver una falla de diseño que la aplicación traía de base, que consistía en almacenar como atributo de la interfaz de usuario un dato que realmente iba asociado al flujo de trabajo. Se ha cambiado la declaración de dicho atributo de las clases que implementan la interfaz de usuario a la clase que implementa los flujos de trabajo.

De igual forma, GeneSys implementaba en sus orígenes una arquitectura modular que admitía la incorporación de nuevas funcionalidades, sin embargo, para el caso concreto del proyecto de esta asignatura, se va a emplear una versión simplificada de la aplicación que reduce su extensibilidad a costa de hacerla más ligera y fácil de entender. Dicha reducción aún está pendiente de realizarse, por lo que de momento la aplicación completa se encuentra en el repositorio.

--------------------------------------------------------------------------------
HITO 2

--------------------------------------------------------------------------------
HITO 3
