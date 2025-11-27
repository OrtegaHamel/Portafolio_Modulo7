from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from propiedades.views import home_propiedades

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_propiedades, name='home_propiedades'),
    path('propiedades/', include('propiedades.urls')),
    path('usuarios/', include('usuarios.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)