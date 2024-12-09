from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalogo/', include('catalogo.urls')),  # Incluye las URLs de la app catalogo
    path('contacto/', include('contacto.urls')),  # Ruta para la app 'contacto'
    path('', include('catalogo.urls')),  # Si deseas que la página de inicio sea del catálogo
    path('pagar/', include('catalogo.urls')),  # Ruta para la página de pago
]
