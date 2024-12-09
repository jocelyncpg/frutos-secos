from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm

def contacto(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Obtener los datos del formulario
            nombre = form.cleaned_data['nombre']
            correo = form.cleaned_data['correo']
            mensaje = form.cleaned_data['mensaje']

            # Enviar el correo (esto puede configurarse más según tus preferencias)
            send_mail(
                f"Nuevo mensaje de {nombre}",
                mensaje,
                correo,
                ['jocperezg@gmail.com'],  # Correo de destino
            )
            return render(request, 'contacto/gracias.html')  # Página de agradecimiento
    else:
        form = ContactForm()

    return render(request, 'catalogo/contacto.html', {'form': form})

# contacto/views.py
def gracias(request):
    return render(request, 'contacto/gracias.html')  # Asegúrate de especificar la ruta completa
