from django.core.exceptions import PermissionDenied
from functools import wraps

def arrendatario_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.tipo_usuario != 'arrendatario':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def administrador_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.tipo_usuario != 'administrador':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def propietario_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.tipo_usuario != 'propietario':
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def propietario_o_administrador_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.tipo_usuario not in ['propietario', 'administrador']:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view