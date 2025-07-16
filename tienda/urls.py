from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CambiarPasswordView

urlpatterns = [
    path('', views.home, name='home'),
    path('producto/<int:pk>/', views.detalle_producto, name='detalle_producto'),

    # Usuario
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/registro/', views.registro, name='registro'),
    path('accounts/perfil/', views.perfil, name='perfil'),
    path('accounts/perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfil/cambiar-password/', CambiarPasswordView.as_view(), name='cambiar_password'),

    # Funciones de tienda
    path('buscar/', views.buscar, name='buscar'),
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    # Productos
    path('producto/nuevo/', views.crear_producto, name='crear_producto'),
    path('producto/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('producto/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    
    # Carrito
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/quitar/<int:producto_id>/', views.quitar_del_carrito, name='quitar_del_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),
    path('carrito/confirmar/', views.confirmar_compra, name='confirmar_compra'),

    # Contacto
    path('contacto/', views.contacto, name='contacto'),
    path('about/', views.about, name='about'),


]
