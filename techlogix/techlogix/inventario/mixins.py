from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PermisoRequeridoMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """Anónimo -> redirige al login. Autenticado sin el permiso -> error 403.
    El permiso se declara en cada vista con `permission_required`."""
