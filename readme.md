**Solución en local**

**Backend**

La solución en local requiere Python en su versión 3.10.x o superior instalado en el sistema y la última versión de “poetry” (gestor de dependencias de python), este a su vez podría necesitar pip o pipx para instalarse.

**Python 3.10.x o superior**

**Poetry**

**Pip y pipx**

**Git CLI.**

Postgres 17 (podría funcionar con versiones anteriores)

Una vez instalados los requerimientos previos, podremos entrar en una carpeta a nuestra elección y abrir en ella un cmd o powershell.

Haremos un clon del repositorio de la aplicación con el siguiente comando.

**Git clone <https://github.com/EdwinDimas/myulibrary_backend.git>**

Activamos el entorno virtual con el comando

**poetry shell**

instalamos todas las dependencias del proyecto

**poetry install**

hay que validar dos grupos de credenciales que deberán estar presentes en la configuración base de django para que sea completamente funcional.

1. Las credenciales de acceso a la base de datos, que requieren nombre de la base de datos, user, password e ip del server para conectarse.
2. Credenciales del servidor CDN de Cloudinary que se ha utilizado como api para facilitar el uso de las imágenes en django. Crearse una cuenta de usuario es gratuito y tiene un tamaño considerable para subir archivos, para este paso se requiere una apikey.

Todas estas modificaciones pueden hacerse dentro del archivo **settings.py**

Para mejorar la experiencia de prueba se han preparado tablas catalogo para rellenar el sistema durante su testeo, estas se cargan a través de los archivos json dentro de la carpeta fixtures, de la siguiente manera

**Python manage.py loaddata “nombre_de_archivo”**

Es importante ejecutarlos todos.

Finalmente, el servidor puede ponerse a funcionar usado Python manage.py runserver, el software indicará en la terminal en que dirección ip y puerto se ha abierto la aplicación.