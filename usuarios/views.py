# usuarios/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import RegistroUsuarioForm
from django.contrib.auth.decorators import login_required
from .models import Usuario, Perfil
from propiedades.models import Propiedad, Arrendamiento
from usuarios.decorators import propietario_required

@login_required
def registrar_usuario(request):
    messages.info(request, 'Ya estás registrado.')
    return redirect('home_propiedades')

# Vista original para usuarios no autenticados
def registrar_usuario(request):
    if request.user.is_authenticated:
        messages.info(request, 'Ya estás registrado.')
        return redirect('home_propiedades')

    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'usuarios/registrar_usuario.html', {'form': form})

@login_required
@propietario_required
def perfil_propietario(request):
    # Obtener el perfil del usuario
    perfil = request.user.perfil

    # Obtener las propiedades del propietario que están arrendadas
    propiedades_en_arrendo = Propiedad.objects.filter(
        propietario=request.user,  
        disponible=False
    ).distinct()

    return render(request, 'usuarios/perfil_propietario.html', {
        'perfil': perfil,
        'propiedades_en_arrendo': propiedades_en_arrendo,
    })

@login_required
def perfil_usuario(request):
    perfil = get_object_or_404(Perfil, usuario=request.user)
    return render(request, 'usuarios/perfil_usuario.html', {'perfil': perfil})

@login_required
def perfil_propietario(request):
    perfil = get_object_or_404(Perfil, usuario=request.user)
    propiedades_en_arrendo = Propiedad.objects.filter(
        propietario=request.user,
        disponible=False
    ).distinct()
    return render(request, 'usuarios/perfil_propietario.html', {
        'perfil': perfil,
        'propiedades_en_arrendo': propiedades_en_arrendo,
    })

def registrar_usuario(request):
    # Aquí puedes implementar la lógica para registrar usuarios
    # Por ahora, dejamos un placeholder
    return render(request, 'usuarios/registrar_usuario.html')