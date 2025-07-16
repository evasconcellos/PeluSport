Proyecto final "Tienda PeluSport" para el curso de Python Flex en Coderhouse comisión 78110

Crear entorno virtual e instalar Django en Powershell:

python -m venv venv 
.\venv\Scripts\activate 
pip install django
python -m pip install Pillow

Migraciones: python manage.py migrate

Cargar productos estáticos: python manage.py cargar_productos

Correr servidor: python manage.py runserver

Entrar a: http://127.0.0.1:8000/

Funcionalidades:

-Registro de usuario
-Inicio de sesión
-Ver productos en home
-Ver detalle de productos del home
-Busqueda de productos
-Agregar opinión sobre el producto
-Agregar producto al carrito
-Eliminar producto del carrito
-Confirmación de compra

-Ver perfil y modificar datos.
-Cambiar contraseña
-Agregar avatar en el perfil, eliminarlo o cambiarlo subiendo una img.

-Form de contacto

------ Crear superuser para administrar mediante tablas--------

En la terminal:

python manage.py createsuperuser

Crear usuario

Volver a correr servidor: python manage.py runserver

Entrar a: http://127.0.0.1:8000/admin e ingresar con el user y contraseña creada.

- Logueandose con un superuser a la web se puede crear, editar y eliminar productos sin necesidad de entrar /admin, con iniciar sesion a la web se desplegan las opciones.

Video demostración de funcionalidades de la web: https://youtu.be/LOUO7Lu3xQ0
