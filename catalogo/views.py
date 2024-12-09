
from django.shortcuts import render, redirect
from .models import Producto
from django.conf import settings
from django.http import HttpResponse

# Vista para crear la preferencia de pago
def crear_preferencia(request):
    # Instancia de MercadoPago con el Access Token
    mp = mercadopago.MP(settings.MERCADOPAGO_ACCESS_TOKEN)

    # Detalles del carrito (estos datos pueden ser dinámicos, por ejemplo, sacados de la base de datos)
    carrito = [
        {"title": "Frutos Secos", "quantity": 2, "unit_price": 500},
        {"title": "Almendras", "quantity": 1, "unit_price": 300},
    ]
    
    # Crear la preferencia de pago
    preference_data = {
        "items": carrito,
        "back_urls": {
            "success": "http://localhost:8000/pago-exitoso/",
            "failure": "http://localhost:8000/pago-fallido/",
            "pending": "http://localhost:8000/pago-pendiente/"
        },
        "auto_return": "approved"
    }
    
    # Crear la preferencia con MercadoPago
    preference = mp.create_preference(preference_data)
    
    # Redirigir al usuario a la URL de pago
    if preference["status"] == 201:
        return redirect(preference["response"]["sandbox_init_point"])  # Redirige a la URL de pago
    else:
        return render(request, 'catalogo/error_pago.html', {'error': 'Hubo un problema al crear la preferencia de pago.'})





def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'catalogo/catalogo.html', {'productos': productos})

def carrito_view(request):
    carrito = request.session.get('carrito', [])
    if not carrito:
        mensaje = "Tu carrito está vacío"
    else:
        total = 0
        for item in carrito:
            total += item['precio'] * item['cantidad']
        total = round(total, 2)

        mensaje = f"Total del carrito: ${total}"

    context = {
        'carrito': carrito,
        'mensaje': mensaje,
    }

    return render(request, 'catalogo/carrito.html', context)



def carrito(request):
    # Obtener los productos en el carrito desde la sesión
    carrito = request.session.get('carrito', [])
    productos_carrito = []
    total = 0

    for item in carrito:
        producto = Producto.objects.get(id=item['id'])
        total += producto.precio * item['cantidad']
        productos_carrito.append({
            'producto': producto,
            'cantidad': item['cantidad'],
            'subtotal': producto.precio * item['cantidad']
        })

    return render(request, 'carrito.html', {
        'productos_carrito': productos_carrito,
        'total': total
    })
def agregar_al_carrito(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    carrito = request.session.get('carrito', {})

    # Si el producto ya está en el carrito, solo actualizamos la cantidad
    if str(producto.id) in carrito:
        carrito[str(producto.id)]['cantidad'] += 1
    else:
        carrito[str(producto.id)] = {
            'nombre': producto.nombre,
            'precio': producto.precio,
            'cantidad': 1
        }

    # Guardamos el carrito actualizado en la sesión
    request.session['carrito'] = carrito

    return redirect('carrito')

# catalogo/views.py
def pago_exitoso(request):
    return render(request, 'catalogo/pago_exitoso.html')

def pago_fallido(request):
    return render(request, 'catalogo/pago_fallido.html')

def pago_pendiente(request):
    return render(request, 'catalogo/pago_pendiente.html')




def pagar(request):
    # Obtener el carrito desde la sesión (ajusta esta parte según cómo manejes el carrito)
    carrito = request.session.get('carrito', {})

    # Si el carrito está vacío, asegúrate de pasar un valor 0
    if not carrito:
        total = 0
    else:
        # Calcula el total sumando los precios de los productos
        total = sum(item['precio'] * item['cantidad'] for item in carrito.values())

    # Agregar al contexto la variable total
    context = {
        'total': total,
        'preference_id': 'tu_preference_id_aqui',  # Asegúrate de tener un preference_id válido
    }

    # Renderiza la plantilla con el contexto
    return render(request, 'catalogo/pagar.html', context)

def procesar_pago(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        monto = request.POST.get("monto")

        # Lógica para simular el pago
        if monto and nombre:
            # Simulamos que el pago fue exitoso si el monto es mayor que cero
            if float(monto) > 0:
                return render(request, 'catalogo/pago_exitoso.html', {'nombre': nombre, 'monto': monto})
            else:
                return render(request, 'catalogo/pago_fallido.html', {'error': "Monto debe ser mayor que 0"})
        else:
            return render(request, 'catalogo/pago_pendiente.html', {'error': "Datos incompletos"})
    else:
        return HttpResponse("Método no permitido", status=405)



def transbank_checkout(request):
    # Asumimos que tienes un carrito de compras en la sesión
    carrito = request.session.get('carrito', {})
    
    # Calcula el total del carrito (esto dependerá de cómo manejas el carrito en tu aplicación)
    total = sum(item['precio'] * item['cantidad'] for item in carrito.values())
    
    # Crea el contexto para pasar a la plantilla
    context = {
        'total': total,  # Agrega el total al contexto
        'preference_id': 'tu_preference_id_aqui',  # Ajusta con tu ID de preferencia de MercadoPago
    }

    return render(request, 'catalogo/transbank_checkout.html', context)
