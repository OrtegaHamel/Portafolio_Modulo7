from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import BusquedaPropiedadesForm, PropiedadForm, ActualizarPreciosForm, ConfirmarEliminacionForm
from django.contrib import messages
from django.db.models import Avg, Max, Min, F
from .models import Propiedad, Arrendamiento, Usuario
from usuarios.models import Arrendamiento, Usuario
from usuarios.decorators import arrendatario_required, administrador_required, propietario_required, propietario_o_administrador_required

def home_propiedades(request):
    form = BusquedaPropiedadesForm(request.GET or None)
    propiedades = Propiedad.objects.filter(disponible=True)

    if form.is_valid():
        tipo = form.cleaned_data.get('tipo')
        dormitorios = form.cleaned_data.get('dormitorios')
        precio_min = form.cleaned_data.get('precio_min')
        precio_max = form.cleaned_data.get('precio_max')
        ubicacion = form.cleaned_data.get('ubicacion')
        ordenar_por = form.cleaned_data.get('ordenar_por')

        if tipo:
            propiedades = propiedades.filter(tipo=tipo)
        if dormitorios:
            propiedades = propiedades.filter(dormitorios=dormitorios)
        if precio_min:
            propiedades = propiedades.filter(precio__gte=precio_min)
        if precio_max:
            propiedades = propiedades.filter(precio__lte=precio_max)
        if ubicacion:
            propiedades = propiedades.filter(ubicacion__icontains=ubicacion)

        # Ordenar resultados
        if ordenar_por == 'precio_asc':
            propiedades = propiedades.order_by('precio')
        elif ordenar_por == 'precio_desc':
            propiedades = propiedades.order_by('-precio')
        elif ordenar_por == 'nombre_asc':
            propiedades = propiedades.order_by('nombre')
        elif ordenar_por == 'nombre_desc':
            propiedades = propiedades.order_by('-nombre')

    return render(request, 'propiedades/home_propiedades.html', {'propiedades': propiedades, 'form': form})

def listar_propiedades(request):
    propiedades = Propiedad.objects.filter(disponible=True)
    return render(request, 'propiedades/listar_propiedades.html', {'propiedades': propiedades})

def detalle_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    return render(request, 'propiedades/detalle_propiedad.html', {'propiedad': propiedad})

@arrendatario_required
def arrendar_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id, disponible=True)
    if Arrendamiento.objects.filter(propiedad=propiedad, arrendatario=request.user).exists():
        messages.error(request, "Ya has arrendado esta propiedad.")
    else:
        Arrendamiento.objects.create(
            propiedad=propiedad,
            arrendatario=request.user,
            fecha_inicio=timezone.now().date()
        )
        propiedad.disponible = False
        propiedad.save()
        messages.success(request, f"Has arrendado {propiedad.nombre} con éxito.")
    return redirect('propiedades:listar_propiedades')

@propietario_o_administrador_required
def crear_propiedad(request):
    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            propiedad = form.save()
            messages.success(request, "Propiedad creada con éxito.")
            return redirect('propiedades:detalle_propiedad', propiedad.id)
    else:
        form = PropiedadForm()
    return render(request, 'propiedades/crear_propiedad.html', {'form': form})

@propietario_o_administrador_required
def editar_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES, instance=propiedad)
        if form.is_valid():
            form.save()
            messages.success(request, "Propiedad actualizada con éxito.")
            return redirect('home_propiedades')
    else:
        form = PropiedadForm(instance=propiedad)
    return render(request, 'propiedades/editar_propiedad.html', {'form': form, 'propiedad': propiedad})

@administrador_required
def eliminar_propiedad(request, propiedad_id):
    propiedad = get_object_or_404(Propiedad, id=propiedad_id)
    if request.method == 'POST':
        propiedad.delete()
        messages.success(request, "Propiedad eliminada con éxito.")
        return redirect('propiedades:listar_propiedades')
    return render(request, 'propiedades/eliminar_propiedad.html', {'propiedad': propiedad})


# Calcular el precio promedio de las propiedades
@administrador_required
def precio_promedio_propiedades(request):
    precio_promedio = Propiedad.objects.aggregate(Avg('precio'))
    return {"precio_promedio": precio_promedio["precio__avg"]}

# Propiedades arrendadas por un usuario específico
@administrador_required
def propiedades_arrendadas_por_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    arrendamientos = usuario.arrendamientos.all()
    return {"usuario": usuario, "arrendamientos": arrendamientos}

# Obtener las propiedades más caras y más baratas
@administrador_required
def propiedades_mas_caras_baratas(request):
    precio_max = Propiedad.objects.aggregate(Max('precio'))
    precio_min = Propiedad.objects.aggregate(Min('precio'))
    propiedad_mas_cara = Propiedad.objects.filter(precio=precio_max["precio__max"]).first()
    propiedad_mas_barata = Propiedad.objects.filter(precio=precio_min["precio__min"]).first()
    return {
        "propiedad_mas_cara": propiedad_mas_cara,
        "propiedad_mas_barata": propiedad_mas_barata,
    }

# Actualizar el precio de todas las propiedades
@administrador_required
def actualizar_precios_propiedades(request):
    if request.method == 'POST':
        form = ActualizarPreciosForm(request.POST)
        if form.is_valid():
            porcentaje = form.cleaned_data['porcentaje']
            Propiedad.objects.all().update(precio=F('precio') * (1 + porcentaje / 100))
            messages.success(request, f"Precios actualizados en un {porcentaje}%.")
            return redirect('home_propiedades')
    else:
        form = ActualizarPreciosForm()
    return render(request, 'propiedades/actualizar_precios.html', {'form': form})




