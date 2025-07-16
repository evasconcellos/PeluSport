from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Incluye todas las rutas de la app 'tienda'
    path('', include('tienda.urls')),

    # Usa las vistas predeterminadas de autenticación de Django
    path('accounts/', include('django.contrib.auth.urls')),
]

# Sirve archivos media en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)