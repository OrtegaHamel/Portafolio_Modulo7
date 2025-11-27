from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('administrador', 'Administrador'),
        ('propietario', 'Propietario'),
        ('arrendatario', 'Arrendatario'),
    ]
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='arrendatario', verbose_name="Tipo de usuario")

    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"
    
class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    direccion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Dirección")
    foto_perfil = models.ImageField(upload_to='perfiles/', verbose_name="Foto de perfil", blank=True, null=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

# usuarios/models.py
class Arrendamiento(models.Model):
    propiedad = models.ForeignKey('propiedades.Propiedad', on_delete=models.CASCADE, related_name='arrendamientos')
    arrendatario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='arrendamientos')
    fecha_inicio = models.DateField(verbose_name="Fecha de inicio")
    fecha_fin = models.DateField(blank=True, null=True, verbose_name="Fecha de fin")

    def __str__(self):
        return f"{self.arrendatario.username} arrenda {self.propiedad.nombre}"
