from django.core.management.base import BaseCommand
from tienda.models import Categoria, Producto
from django.core.files import File
import os

class Command(BaseCommand):
    help = 'Carga productos y categorías de ejemplo con imágenes'

    def handle(self, *args, **kwargs):
        base_dir = os.path.join('tienda', 'static', 'img', 'productos')

        categorias = {
            'Indumentaria': ['Camiseta River Plate', 'Buzo Puma Evostripe'],
            'Accesorios': ['Pelota fútbol AFA', 'Palo de Hockey', 'Gorra Nike'],
            'Calzado': ['Zapatillas Nike Air Max Nuaxis'],
        }

        productos_info = {
            'Camiseta River Plate': {'descripcion': 'Camiseta titular River Plate 2025', 'precio': 119000.00, 'imagen': 'remera_riverplate.jpg'},
            'Buzo Puma Evostripe': {'descripcion': 'El Buzo Puma Evostripe Hombre se adapta a tus movimientos con un diseño ergonómico y deportivo', 'precio': 111700.00, 'imagen': 'buzo_puma.jpg'},
            'Pelota fútbol AFA': {'descripcion': 'Pelota Fútbol Adidas Selección Argentina League 2024', 'precio': 83000.00, 'imagen': 'pelota_afa.jpg'},
            'Palo de Hockey': {'descripcion': 'El Palo Hockey TK Midi es perfecto para jugadores de todas las edades y niveles.', 'precio': 50000.00, 'imagen': 'Palo_hockey.jpg'},
            'Gorra Nike': {'descripcion': 'Gorra con logo de Nike, ideal para días calurosos.', 'precio': 30000.00, 'imagen': 'gorra.jpg'},
            'Zapatillas Nike Air Max Nuaxis': {'descripcion': 'Cómodas y resistentes zapatillas para correr.', 'precio': 120000.00, 'imagen': 'zapatillas_nike.jpg'},
        } 

        for cat_nombre, productos in categorias.items():
            categoria, _ = Categoria.objects.get_or_create(nombre=cat_nombre)
            for producto_nombre in productos:
                datos = productos_info[producto_nombre]
                imagen_path = os.path.join(base_dir, datos['imagen'])

                if not os.path.exists(imagen_path):
                    self.stdout.write(self.style.WARNING(f"No se encontró la imagen: {imagen_path}"))
                    continue

                if not Producto.objects.filter(nombre=producto_nombre).exists():
                    with open(imagen_path, 'rb') as f:
                        producto = Producto(
                            nombre=producto_nombre,
                            descripcion=datos['descripcion'],
                            precio=datos['precio'],
                            categoria=categoria
                        )
                        producto.imagen.save(datos['imagen'], File(f), save=True)
                        self.stdout.write(self.style.SUCCESS(f"Producto cargado: {producto_nombre}"))
                else:
                    self.stdout.write(f"Producto ya existe: {producto_nombre}")