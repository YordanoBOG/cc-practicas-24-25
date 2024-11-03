Hito 2: Integración continua

--------------------------------------------------------------------------------

Vamos a usar GitHub actions como sistema de integración continua, ya que se encuentra incorporado en GitHub y permite integrar con fluidez los tests que vamos a realizar.

Emplearemos la biblioteca de aserciones pytest para hacer los tests en Python, ya que es la biblioteca estándar para este tipo de tareas en el lenguaje, lo que facilita diseñar los tests y evitar problemas de integridad.

Usaremos un archivo yml como gestor de tareas, que estará configurado para instalar las dependencias necesarias para los tests y realizar las pruebas con pytest cada vez que se haga un push en el repositorio de GitHub.

--------------------------------------------------------------------------------

Antes de implementar los test, realizamos una pequeña modificación sobre la aplicación: eliminamos las primeras pantallas/módulos que se lanzaban al ejecutar GeneSys, para que la arquitectura sea más sencilla. Originalmente, GeneSys estaba orientada a poseer una gran extensibilidad. Con este cambio, simplificamos el código para que sea menos complejo a costa de reducir la extensibilidad, ya que en la asignatura de CC nos vamos a centrar en emplear las funciones que GeneSys ofrece, no a incorporar otras nuevas.

Tras modificar la aplicación, preparamos GitHub actions para ejecutar un script yml que instalará dependencias y lanzará el fichero Python que ejecutará varios tests de prueba sobre GeneSys cada vez que se haga un push. Creamos un nuevo archivo en nuestro repositorio de GitHub en una carpeta nueva: .github/workflows/genesys_tests.yml.

![Captura desde 2024-11-02 16-58-39](https://github.com/user-attachments/assets/e5e85881-c54f-4f92-94d8-3034bbd6cad2)

El .yml está configurado para que, cada vez que se haga un push, se instalen las dependencias necesarias en un entorno Ubuntu de la misma versión que el Ubuntu de nuestra máquina local (22.04) y a continuación se lance el archivo tests_hito2.py con la biblioteca pytest, y especificando el directorio de GitHub actual como el entorno del que tomar las rutas relativas para los tests.

![Captura desde 2024-11-03 14-44-34](https://github.com/user-attachments/assets/a1aeb01e-d740-4826-8b16-46024b2600f3)

Entre las dependencias instaladas vía yml, se incluye la instalación de un set de herramientas de línea de comandos que sirven para manipular datos genéticos llamadas bvbrc-cli, y se instalan llamando a dpkg sobre un archivo .deb que se encuentra incluido en el repositorio, y que contiene esas herramientas.

![Captura desde 2024-11-03 12-52-50](https://github.com/user-attachments/assets/52dbb4ae-3a04-44ee-a62e-6f862bcc6ea2)

El resto de dependencias están especificadas en el archivo requirements.txt del repositorio.

![Captura desde 2024-11-03 12-52-28](https://github.com/user-attachments/assets/0230b6c2-b0c9-4bdf-a757-26f8316469da)

De primeras, en tests_hito2.py solo se incluye una prueba exitosa para verificar que el yml funciona.

![Captura desde 2024-11-03 13-25-44](https://github.com/user-attachments/assets/0c30b699-970e-4224-8406-6bbf2f9c8e3d)

Hacemos un push y en la pestaña actions de GitHub podemos ver que el archivo se ha ejecutado correctamente.

![Captura desde 2024-11-03 13-25-33](https://github.com/user-attachments/assets/9665d238-6b30-4bb4-a217-0dc6b4faa278)

Ahora transformamos el archivo en un verdadero ejecutor de tests de GeneSys. Nos centraremos en testear la lógica interna de la aplicación para corroborar que se puede definir, guardar, cargar y ejecutar un flujo de trabajo correctamente. Definimos un flujo de trabajo como variable global y ejecutamos un primer test que comprueba la correcta integridad del flujo creado.

![Captura desde 2024-11-03 15-44-49](https://github.com/user-attachments/assets/02333a2a-e1d1-4254-9ebd-14aaf0949db8)

Después definimos otro test que crea las 5 tareas de preprocesamiento que la aplicación va a llevar a cabo y las añade al flujo de trabajo.

![Captura desde 2024-11-03 15-45-08](https://github.com/user-attachments/assets/e0f9a582-a973-404c-87bf-57033c95866e)

Las siguientes dos pruebas testean las funciones de guardado y carga del flujo de trabajo. Guardamos el flujo, lo vaciamos de tareas y lo cargamos de nuevo a partir de los datos guardados.

![Captura desde 2024-11-03 15-45-18](https://github.com/user-attachments/assets/85ff7fbc-ec9a-488e-a4cb-2d5d3b5a831a)

Por último, ejecutamos el flujo de trabajo. Si las tareas estás correctamente definidas en él, devolverá un 0 en la variable returned_value una vez se haya ejecutado, así que comprobamos esa variable tras la ejecución.

![Captura desde 2024-11-03 15-45-27](https://github.com/user-attachments/assets/273e54d4-76e3-492f-b765-c126bebf398c)

Hacemos un push y comprobamos que los tests se han ejecutado correctamente.

![Captura desde 2024-11-03 15-45-37](https://github.com/user-attachments/assets/d22efba4-413c-4001-8698-367f63ff3525)
