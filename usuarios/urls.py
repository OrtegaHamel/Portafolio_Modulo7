# usuarios/urls.py
from django.urls import path
from .views import perfil_usuario, perfil_propietario, registrar_usuario

app_name = 'usuarios'

urlpatterns = [
    path('perfil/', perfil_usuario, name='perfil_usuario'),
    path('perfil/propietario/', perfil_propietario, name='perfil_propietario'),
    path('registrar/', registrar_usuario, name='registrar_usuario'),
]
