# usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

class RegistroUsuarioForm(UserCreationForm):
    TIPO_USUARIO_CHOICES = [
        ('propietario', 'Propietario'),
        ('arrendatario', 'Arrendatario'),
    ]

    tipo_usuario = forms.ChoiceField(
        choices=TIPO_USUARIO_CHOICES,
        label="Tipo de usuario",
        required=True
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'tipo_usuario']
