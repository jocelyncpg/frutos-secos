# contacto/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.contacto, name='contacto'),  # Ruta para mostrar el formulario
    path('gracias/', views.gracias, name='gracias'),
    
]
