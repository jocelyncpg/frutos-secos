
# catalogo/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogo, name='catalogo'),
    path('carrito/', views.carrito_view, name='carrito'),
    path('pagar/', views.pagar, name='pagar'),  # Asegúrate de tener esta línea
    path('crear-preferencia/', views.crear_preferencia, name='crear_preferencia'),
    path('pago-exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago-fallido/', views.pago_fallido, name='pago_fallido'),
    path('pago-pendiente/', views.pago_pendiente, name='pago_pendiente'),
    path('transbank_checkout/', views.transbank_checkout, name='transbank_checkout'),

]

