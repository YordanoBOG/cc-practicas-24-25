Hito 2: Integración continua
Objetivo

El principal objetivo de este hito es añadir tests y la infraestructura virtual de la aplicación, gestores de dependencias y/o tareas necesarias para que se ejecuten los tests, además de añadir integración continua (CI) al proyecto.

Explicación

En sistemas de desarrollo ágil cada entidad tiene que asegurar que pasa todos los tests antes de ser desplegada. Para ello se escriben una serie de pruebas, (generalmente) fuera del código en sí de la aplicación, como scripts independientes, que se deben siempre pasar al añadir, solicitar cambios (mediante PR) o modificar código. Estos tests tienen el fin obvio de asegurar la calidad del mismo, pero también en un entorno de desarrollo colaborativo permiten integrar código fácilmente asegurándose de que no se rompa nada; por otro lado, permiten también la creación de un entorno en el que se defina de forma precisa la infraestructura necesaria para crear el proyecto. En este hito lo que haremos será configurar nuestro repositorio para que se pasen los tests automáticamente.

Preparar un proyecto para integración continua implica varios pasos:

    Elegir el gestor de tareas desde donde se deberán ejecutar los test.
    Elegir una biblioteca de aserciones que permita llevar a cabo, fácilmente, la comparación entre resultado esperado y obtenido. Esta elección se tiene que llevar a cabo incluso cuando el lenguaje incluya una biblioteca de aserciones estándar. Puede haber bibliotecas más potentes, o simplemente usar otro estilo: generalmente se confronta TDD frente a BDD, pero por eso precisamente tienes que justificar el estilo elegido.
    Buscar un sistema de prueba del código, es decir, un test runner que encuentre, ejecute y escriba informes sobre los tests siguiendo las buenas prácticas en el lenguaje correspondiente. Se tratará, en general, de una librería o marco, casi siempre acompañada de una herramienta de línea de órdenes, que siga los estándares y sea flexible; como en el caso anterior, también se tiene que justificar esa elección, porque en la mayoría de los lenguajes habrá varias opciones donde elegir. En algunos casos los test runners son parte de un testing framework que incluye también bibliotecas de aserciones, pero se tendrá que justificar la elección de cada uno de ellos de forma independiente".
    Integrar las pruebas dentro de las herramientas de construcción del proyecto usando las convenciones estándar de la herramienta y el lenguaje; por ejemplo, incluir un objetivo make test dentro de un Makefile (si ese es el gestor de tareas que se ha elegido). El uso de estas herramientas de construcción permite que tanto en local como en remoto, se lancen los tests exactamente de la misma forma.
    Buscar un sistema online de prueba del código que sea estándar y flexible, es decir, una web gratuita de integración continua tal como GitHub Actions.
    Finalmente, tras darse de alta, configurar el sistema de integración continua de forma que lance los tests automáticamente. Se puede usar Circle-CI, Jenkins, Travis, GitHub Actions, en general cualquier sistema que se pueda conectar a GitHub, es decir, que se active automáticamente al hacer un push a tu repositorio en GitHub. También se pueden usar varios, GitHub envía automáticamente un mensaje a todos los sistemas configurados cuando se hace push, siempre que estén configurados.

Esta fase de integración continua es esencial para el posterior despliegue en un PaaS o IaaS sobre el que se probarán técnicas de despliegue continuo.

Entrega de la práctica

Se tendrá que haber actualizado el repositorio y añadir al fichero de este hito el nombre del proyecto y un enlace al mismo y hacer un pull request.
Valoración

Esta es la puntuación de las diferentes rúbricas. En todas ellas se tendrá que tener en cuenta que lo importante no es la "elección correcta", sino mostrar que el estudiante tiene madurez para tomar una decisión técnica que afectará al resto del proyecto.

    1.5 puntos: Elección y configuración del gestor de tareas.
    1.5 puntos: Elección y uso de la biblioteca de aserciones.
    1.5 puntos: Elección y uso del marco de pruebas.
    4 puntos: Integración continua funcionando y correcta justificación del sistema elegido.
    1.5 puntos: Correcta implementación y ejecución de los tests para testear algunos aspectos de la lógica de negocio de la aplicación a desarrollar.

--------------------------------------------------------------------------------

¿Qué es un gestor de tareas? Make, por ejemplo: un archivo que ejecuta determiandas tareas. Invoke en Python.
¿Biblioteca de aserciones? pytest: biblioteca para hacer tests de código en Python. Sirve para comprobar que el test devuelve el resultado que toca.
¿Marco de pruebas? Entorno desde el que se realizan los tests. Después usas GitHub action para automatizar que se ejecute un test cada vez que se haga un push.

Proceso del hito 2.
La idea es que al hacer un push, esté definido con GitHub actions que se lance la aplicación GeneSys. Después, GitHub actions ejecuta los tests definidos en pytest, que se llaman a través de invoke (pip install invoke/sudo apt install python3-invoke. Llamas a invoke escribiendo invoke en la terminal). Hay que configurar el entorno de pruebas en GitHub con todas las bibliotecas que requiere la aplicación, probablemente crearte un entorno virtual Python.

--------------------------------------------------------------------------------

Antes de implementar los test, realizamos la siguiente modificación sobre la aplicación: eliminamos las primeras pantallas/módulos que se lanzaban al ejecutar GeneSys, para que la arquitectura sea más sencilla. Originalmente, GeneSys estaba orientada a poseer una gran extensibilidad. Con este cambio, simplificamos el código para que sea menos complejo a costa de reducir la extensibilidad, ya que en la asignatura de CC nos vamos a centrar en emplear las funciones que GeneSys ofrece, no a incorporar otras nuevas.

Tras modificar la aplicación, preparamos GitHub actions para ejecutar un script Python que empleará la biblioteca invoke para ejecutar varios tests de prueba sobre GeneSys cada vez que se haga un push. Creamos un nuevo archivo en nuestro repositorio de GitHub en una carpeta nueva: .github/workflows/genesys_tests.yml.

![Captura desde 2024-11-02 16-58-39](https://github.com/user-attachments/assets/e5e85881-c54f-4f92-94d8-3034bbd6cad2)

El .yml está configurado para que, cada vez que se haga un push, se instalen las dependencias especificadas en requirements.txt en un entorno Ubuntu de la misma versión que el Ubuntu de nuestra máquina local (22.04) y a continuación se lance el archivo tests_hito2.py con la función pytest de la biblioteca invoke.

![Captura desde 2024-11-03 13-21-41](https://github.com/user-attachments/assets/29f53a42-7e13-4f75-bd7f-3f3239074f9a)

Entre las dependencias instaladas vía yml, se incluye la instalación de un set de herramientas de línea de comandos que sirven para manipular datos genéticos llamadas bvbrc-cli, y se instalan llamando a dpkg sobre un archivo .deb que se encuentra incluido en el repositorio, y que contiene esas herramientas.

![Captura desde 2024-11-03 12-52-50](https://github.com/user-attachments/assets/52dbb4ae-3a04-44ee-a62e-6f862bcc6ea2)

El resto de dependencias están especificadas en el archivo requirements.txt del repositorio.

![Captura desde 2024-11-03 12-52-28](https://github.com/user-attachments/assets/0230b6c2-b0c9-4bdf-a757-26f8316469da)

De primeras, en tests_hito2.py solo se incluye una prueba exitosa para verificar que el yml funciona.

![Captura desde 2024-11-03 13-25-44](https://github.com/user-attachments/assets/0c30b699-970e-4224-8406-6bbf2f9c8e3d)

Hacemos un push y en la pestaña actions de GitHub podemos ver que el archivo se ha ejecutado correctamente.

![Captura desde 2024-11-03 13-25-33](https://github.com/user-attachments/assets/9665d238-6b30-4bb4-a217-0dc6b4faa278)

Ahora transformamos el archivo en un verdadero ejecutor de tests de GeneSys.
