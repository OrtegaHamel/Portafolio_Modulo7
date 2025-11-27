# propiedades/urls.py
from django.urls import path
from .views import (
    listar_propiedades,
    detalle_propiedad,
    crear_propiedad,
    editar_propiedad,
    eliminar_propiedad,
    arrendar_propiedad,
    precio_promedio_propiedades,
    propiedades_arrendadas_por_usuario,
    propiedades_mas_caras_baratas,
    actualizar_precios_propiedades,
)

app_name = 'propiedades'

urlpatterns = [
    # --- Acciones para todos los usuarios ---
    path('', listar_propiedades, name='listar_propiedades'),
    path('detalle/<int:propiedad_id>/', detalle_propiedad, name='detalle_propiedad'),

    # --- Acciones para Arrendatarios ---
    path('arrendar/<int:propiedad_id>/', arrendar_propiedad, name='arrendar_propiedad'),

    # --- Acciones para Propietarios y Administradores ---
    path('crear/', crear_propiedad, name='crear_propiedad'),
    path('editar/<int:propiedad_id>/', editar_propiedad, name='editar_propiedad'),

    # --- Acciones para Administradores ---
    path('eliminar/<int:propiedad_id>/', eliminar_propiedad, name='eliminar_propiedad'),
    path('admin/precio-promedio/', precio_promedio_propiedades, name='precio_promedio'),
    path('admin/arrendamientos/<int:usuario_id>/', propiedades_arrendadas_por_usuario, name='arrendamientos_usuario'),
    path('admin/propiedades-extremas/', propiedades_mas_caras_baratas, name='propiedades_extremas'),
    path('admin/actualizar-precios/', actualizar_precios_propiedades, name='actualizar_precios'),
]
