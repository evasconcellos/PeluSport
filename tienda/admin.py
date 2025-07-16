from django.contrib import admin
from .models import Producto, Categoria, Perfil, Review, Contacto

admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Perfil)
admin.site.register(Review)
admin.site.register(Contacto)

