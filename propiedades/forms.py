from django import forms
from .models import Propiedad

class BusquedaPropiedadesForm(forms.Form):
    TIPO_PROPIEDAD_CHOICES = [
        ('', 'Todos los tipos'),
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('estacionamiento', 'Estacionamiento'),
    ]

    ORDENAR_POR_CHOICES = [
        ('precio_asc', 'Precio (ascendente)'),
        ('precio_desc', 'Precio (descendente)'),
        ('nombre_asc', 'Nombre (A-Z)'),
        ('nombre_desc', 'Nombre (Z-A)'),
    ]

    tipo = forms.ChoiceField(choices=TIPO_PROPIEDAD_CHOICES, required=False, label="Tipo de propiedad")
    dormitorios = forms.IntegerField(required=False, min_value=0, label="Número de dormitorios")
    precio_min = forms.DecimalField(required=False, min_value=0, label="Precio mínimo")
    precio_max = forms.DecimalField(required=False, min_value=0, label="Precio máximo")
    ubicacion = forms.CharField(required=False, label="Ubicación")
    ordenar_por = forms.ChoiceField(choices=ORDENAR_POR_CHOICES, required=False, label="Ordenar por")


class PropiedadForm(forms.ModelForm):
    class Meta:
        model = Propiedad
        fields = [
            'nombre',
            'tipo',
            'ubicacion',
            'metros_cuadrados',
            'dormitorios',
            'descripcion',
            'precio',
            'foto',
            'disponible',
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

# Actualizar precios de propiedades
class ActualizarPreciosForm(forms.Form):
    porcentaje = forms.DecimalField(
        label='Porcentaje de aumento/disminución',
        max_digits=5,
        decimal_places=2,
        min_value=-100,  # Permite disminuir hasta 100%
        max_value=1000,  # Permite aumentar hasta 1000%
        help_text='Ingresa un valor positivo para aumentar o negativo para disminuir (ej: 10 para aumentar 10%, -5 para disminuir 5%).'
    )

# Confirmar eliminación de propiedad
class ConfirmarEliminacionForm(forms.Form):
    confirmar = forms.BooleanField(
        label='Confirmo que deseo eliminar esta propiedad',
        required=True
    )
