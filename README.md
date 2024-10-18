# CC-Practicas-24-25
Cloud Computing subject project.

En cada hito el fichero README.md describirá el estado del proyecto actual, y se sacará a otros ficheros (enlazándolos) la documentación adicional que haya podido necesitarse para la corrección de otros hitos. Subir los ficheros actualizados a GitHub y hacer un pull request para cada hito completado. Respecto a la documentación sobre la realización de este proyecto, conviene que se cree un documento aparte usando los diferentes mecanismos que ofrece GitHub y se enlace desde el fichero donde se explique el proyecto, en el directorio principal. O sea, incluir en este readme los enlaces a la documentación. La documentación se incluirá en ficheros Markdown.

--------------------------------------------------------------------------------
HITO 1

Primero, se crea un nuevo repositorio en GitHub con la ruta «git remote add origin git@github.com:YordanoBOG/CC-Practicas-24-25.git». Se crea un repositorio público con la licencia GNU General Public License v3.0.

Antes de seguir, es necesario generar un par de claves pública/privada en GitHub para que los repositorios de GitHub se enlacen a nuestra máquina, y cada vez que se realice una orden de subida o bajada al repositorio, se realice sin necesidad de autenticación manual. Seguimos el manual de la siguiente dirección: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent y generamos un nuevo par de claves SSH pública y privada en nuestro ordenador en las rutas «/home/bruno/.ssh/id_ed25519» (privada) y «/home/bruno/.ssh/id_ed25519.pub» (pública). Si analizamos el contenido de la clave pública, se nos devuelve lo siguiente:

![Captura desde 2024-10-18 18-32-22](https://github.com/user-attachments/assets/75aacc20-a812-4641-8aae-6fa33f31125d)

En la configuración del perfil de GitHub, en el apartado «SSH and GPG keys», existe la opción de añadir una nueva clave pública con el botón «New SSH key». Se siguen los pasos de: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account y se añade la clave pública recién creada a GitHub. Ya tenemos la máquina de trabajo ligada a nuestro repositorio.

![Captura desde 2024-10-18 19-05-38](https://github.com/user-attachments/assets/03e8039a-7bed-427e-915c-8badd3cd3415)

Ya podemos crear un repositorio con git en nuestra carpeta de trabajo. Primero se copian a la ruta de trabajo aquellos archivos que conformarán la base para nuestra aplicación, que va a ser una adaptación a la nube de mi trabajo fin de grado (y cuyos detalles se exponen más adelante). Después, se ejecutan los siguientes comandos: «git init», «git add README.md», «git commit -m "first commit"», «git branch -M main», «git remote add origin git@github.com:YordanoBOG/CC-Practicas-24-25.git» y «git push -u origin main».

Con esto, ya hemos añadido los archivos con los que vamos a trabajar al repositorio. Realizamos un par de ajustes finales consistentes en crear un archivo .gitignore, que de momento permanecerá vacío, y en editar el archivo README.md para documentar los avances realizados en la práctica.

Así se ve el repositorio en nuestra máquina local.

![Captura desde 2024-10-18 19-09-31](https://github.com/user-attachments/assets/95a951fb-f13b-48e0-8745-a4d25a3db818)

Y así se ve en el repositorio de GitHub.

![Captura desde 2024-10-18 19-24-42](https://github.com/user-attachments/assets/f846227c-3c82-47c5-8ce5-4cbb4280a7d1)

A continuación se describe el proyecto de prácticas que se va a implementar.

El presente proyecto de cloud computing pretende desplegar en la nube la aplicación diseñada en mi trabajo fin de grado (https://github.com/YordanoBOG/GeneSys). La aplicación en cuestión se llama GeneSys y permite preprocesar datos proteicos descargados de la base de datos genómica del Bacterial and Viral Bioinformatics Resource Center (https://www.bv-brc.org/) a través de un flujo personalizado por el usuario. La aplicación está diseñada casi en su totalidad en Python, con Kivy para la interfaz de usuario. Al ser una herramienta de procesado de datos, su despliegue en la nube tiene sentido, ya que habilitaría que los usuarios puedan procesar un mayor volumen de datos del que podrían estando limitados por la potencia de sus equipos de trabajo personales.

El problema que pretende resolver esta aplicación es uno de los pasos que se llevaron a cabo para realizar la siguiente publicación: https://academic.oup.com/nar/article/48/22/12632/6020195?login=false, donde se lleva a cabo un análisis de proteínas vecinas a partir de unas muestras previamente preprocesadas. GeneSys permite automatizar dicho preprocesado de los datos empleados en el estudio para que así se pueda repetir el experimento con más facilidad en el futuro, e incluso empleando proteínas con características diferentes como objeto de estudio.

En concreto, las funcionalidades que proporciona la aplicación son las siguientes:
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

Por último, definimos un issue consistente en almacenar como atributo de la interfaz de usuario un dato que realmente iba asociado al flujo de trabajo; un bug que la aplicación del trabajo fin de grado traía de base y que aprovechamos para resolver ahora.

![Captura desde 2024-10-18 19-29-47](https://github.com/user-attachments/assets/5bf9288f-eb5f-4788-893b-2ca472c89bae)
![Captura desde 2024-10-18 19-31-43](https://github.com/user-attachments/assets/e75cef88-fbb2-4e8f-bd43-48cd30c8b27d)

Junto a él, se definen más issues que nos ayudarán a organizarnos de cara a las tareas del hito 2, si bien aún no se resuelven.

![Captura desde 2024-10-18 19-29-30](https://github.com/user-attachments/assets/c7f196c1-253d-4296-a5a9-1dc6e68eb341)

En resumen, se ha creado un nuevo repositorio en GitHub, se le han añadido los ficheros de la aplicación y se ha aprovechado para resolver una falla de diseño que la aplicación traía de base.

--------------------------------------------------------------------------------
HITO 2

Modificamos la aplicación del TFG para transformarla en una aplicación que pueda aprovechar todas las ventajas de la nube. Realizamos las siguientes modificaciones sobre el código original:

-> Reducimos la funcionalidad de la aplicación para que la arquitectura sea más sencilla. Originalmente, GeneSys estaba orientada a poseer una gran extensibilidad. Simplificamos el código para que sea menos complejo a costa de reducir la extensibilidad, ya que en la asignatura de CC nos vamos a centrar en emplear las funciones que GeneSys ofrece, no a incorporar otras nuevas.

-> Implementamos un sistema de gestión de usuarios. En la nube, que solo los usuarios autorizados puedan acceder a la aplicación es fundamental. Modificamos la pestaña inicial de la aplicación para incluir un sistema de autenticación de usuarios. La aplicación original permite guardar flujos de trabajo en ficheros json, así como cargarlos desde ellos. Creamos dos roles de usuario, uno básico y otro premium. La idea es simular que el usuario premium es toda persona que pague por disponer de las funcionalidades de la aplicación que permiten guardar y cargar flujos de trabajo GeneSys usando ficheros .json.

-> En hitos posteriores, cuando despleguemos una base de datos en un contenedor, los usuarios y sus contraseñas se almacenarán en ella. De momento, contamos con un usuario básico y otro premium (más sus contraseñas) de prueba en un fichero .json.

--------------------------------------------------------------------------------
HITO 3
