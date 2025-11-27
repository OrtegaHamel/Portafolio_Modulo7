from django.db import models
from usuarios.models import Usuario, Arrendamiento

class Propiedad(models.Model):
    TIPO_PROPIEDAD_CHOICES = [
        ('casa', 'Casa'),
        ('departamento', 'Departamento'),
        ('estacionamiento', 'Estacionamiento'),
    ]

    nombre = models.CharField(max_length=100, verbose_name="Nombre de la propiedad")
    tipo = models.CharField(max_length=20, choices=TIPO_PROPIEDAD_CHOICES, verbose_name="Tipo de propiedad")
    ubicacion = models.CharField(max_length=200, verbose_name="Ubicación")
    metros_cuadrados = models.PositiveIntegerField(verbose_name="Metros cuadrados")
    dormitorios = models.PositiveIntegerField(default=1, verbose_name="Número de dormitorios")  # Nuevo campo
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    disponible = models.BooleanField(default=True, verbose_name="Disponible para arrendar")
    foto = models.ImageField(upload_to='propiedades/', verbose_name="Foto de la propiedad", blank=True, null=True)
    propietario = models.ForeignKey(
        'usuarios.Usuario',
        on_delete=models.CASCADE,
        related_name='propiedades',
        verbose_name="Propietario",
        null=True,  # Permite que el campo sea nulo temporalmente
        blank=True,  # Permite que el campo esté vacío en formularios
    )

    def __str__(self):
        return f"{self.nombre} ({self.get_tipo_display()})"

