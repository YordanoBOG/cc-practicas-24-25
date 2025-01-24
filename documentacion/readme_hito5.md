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

![Captura desde 2025-01-24 11-19-54](https://github.com/user-attachments/assets/14236c62-25e8-4d63-b3ac-7f8e7d7e9fdc)

Ambos servicios se encuentran accesibles en el servicio principal de la aplicación a através de variables de entorno, y poseen sus propios ficheros Dockerfile.

El dockerfile de mongo especifica la imagen de Mongo a usar, la ruta a la base de datos en el contenedor y el puerto desde el que acceder a ella:

![Captura desde 2025-01-24 11-22-31](https://github.com/user-attachments/assets/d7b0dae9-5fd3-481a-8508-a8f5fcabe2d9)

Y el dockerfile del logger, lo mismo:

![Captura desde 2025-01-24 11-22-35](https://github.com/user-attachments/assets/c44fe966-dc3f-4320-8feb-930e4f38a058)

Sin embargo, al redesplegar el servicio, los endpoints de la base de datos siguen sin funcionar.

Para averiguar lo que ocurre, creamos un nuevo servicio por separado de Mongo en Render, solo que esta vez lo desplegamos como servicio web, ya que solo lo vamos a usar para encontrar la configuración de despliegue adecuada para nuestro Dockerfile de mongo. Especificamos dicho Dockerfile en la configuración del servicio.

![Captura desde 2025-01-24 11-29-04](https://github.com/user-attachments/assets/c653774d-aaa6-4af9-899d-7095c3c1110c)
![Captura desde 2025-01-24 11-29-20](https://github.com/user-attachments/assets/9aae4c32-3a5f-44d0-9c47-e14452ebcde7)
![Captura desde 2025-01-24 11-29-26](https://github.com/user-attachments/assets/f40a53ca-9214-4478-af48-81cb7d50e73c)

Hacemos un push y comprobamos la terminal log del servicio.

![Captura desde 2025-01-24 11-35-27](https://github.com/user-attachments/assets/ec20ea36-d459-406d-ad6d-08c9619f18ee)

Vemos que da un error relacionado con las claves SSL. Esto se debe a que el cliente de Render requiere una conexión a Mongo usando este tipo de claves, que típicamente se obtienen a través de organizaciones certificadas. Dado que no tenemos ninguna clave proporcionada por ninguna organización, vamos a intentar generarla por nuestra cuenta usando una organización inexistente de ejemplo.

Para incluir una clave SSL en nuestro repositorio usamos el comando "openssl genrsa -out ca.key 4096", que genera un archivo ca.key con una clave privada. Luego, usamos "openssl req -x509 -new -nodes -key ca.key -sha256 -days 365 -out ca.crt -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=example.com"" para generar un archivo ca.crt con el certificado a validar usando dicha clave. Se puede apreciar que las credenciales usadas en el comando pertenecen a una organizaicón inexistente.

Repetimos el proceso para la instancia de Mongo, con "openssl genrsa -out mongodb.key 4096" para generar la clave privada de la base de datos Mongo en el archivo mongo.key, y "openssl req -new -key mongodb.key -out mongodb.csr -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=mongo-db"" para el certificado en el archivo mongo.csr. Además, combinamos ambos documentos en un nuevo documento mongodb.pem con "cat mongodb.key mongodb.crt > mongodb.pem".

Metemos todos los documentos en una carpeta específica en el repositorio.

![Captura desde 2025-01-24 11-47-11](https://github.com/user-attachments/assets/190e4124-039a-41e7-8fcd-15891f91a1c5)

Y actualizamos el Dockerfile de despliegue de Mongo.

![Captura desde 2025-01-24 11-51-28](https://github.com/user-attachments/assets/44c092bb-71c5-47bb-a71b-5269a02a443a)

Relanzamos el servicio y miramos los logs de mongo_db. Vemos que el servicio se queda un buen rato desplegándose hasta que finalmente falla, probablemente debido a que no se ha encontrado ninguna clave asociada a la que hemos creado (porque pertenece a una organización ficticia), lo que ha provocado que el servicio se cuelgue hasta que ha pasado el tiempo de respuesta límite permitido y se ha detenido.

![Captura desde 2025-01-24 12-03-23](https://github.com/user-attachments/assets/183697e7-1489-4027-88b0-0c5d119242be)
![Captura desde 2025-01-24 12-09-32](https://github.com/user-attachments/assets/a7620125-cf20-447a-b32d-b49c58f2d02b)

Intentamos una última solución consistente en desplegar la base de datos mongo como un servicio adicional siguiendo la propia guía de render para desplegar una instancia de mongo (https://render.com/docs/deploy-mongodb).

![Captura desde 2025-01-24 12-11-19](https://github.com/user-attachments/assets/95494444-7514-4fc6-a603-425c49389f9f)

Se nos dice que debemos realizar el despliegue como servicio privado.

![Captura desde 2025-01-24 12-12-30](https://github.com/user-attachments/assets/bee08f44-9697-46f5-aba8-9033ff598fa4)

Especificamos la ruta al repositorio de GitHub que se nos da: https://github.com/render-examples/mongodb. Pero cuando llegamos a la pestaña de configuración, vemos que el servicio no tiene una opción gratuita.

![Captura desde 2025-01-24 12-13-49](https://github.com/user-attachments/assets/22c2039d-0512-40c2-ae87-c5a01681d154)

Por tanto, si bien el despliegue de la aplicación ha sido exitoso, el hecho de que no podamos usar Postgre para la base de datos nos impide generar un servicio de base de datos como nos gustaría, lo que hace que la aplicación no sirva para casi nada en el PaaS, ya que GeneSys, tal y como se ha planteado a lo largo de la asignatura, es un sistema especializado en procesar información documental bioinformática en un entorno contenerizado.
