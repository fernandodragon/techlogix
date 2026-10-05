"""Crea los grupos Administrador / Asistente, sus permisos y los usuarios de prueba.

Uso:  python manage.py setup_roles
"""
import os

from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from inventario.models import Categoria, Producto

ROLES = {
    "Administrador": ["add", "change", "delete", "view"],  # CRUD completo
    "Asistente": ["view"],                                  # solo lectura
}
USUARIOS = [
    ("admin_tech", "Administrador", "ADMIN_TECH_PASSWORD", "Admin_Tech_2026"),
    ("asistente_tech", "Asistente", "ASISTENTE_TECH_PASSWORD", "Asist_Tech_2026"),
]


class Command(BaseCommand):
    help = "Crea grupos, permisos y usuarios de prueba (idempotente)."

    def handle(self, *args, **options):
        for nombre, acciones in ROLES.items():
            grupo, _ = Group.objects.get_or_create(name=nombre)
            permisos = []
            for modelo in (Producto, Categoria):
                ct = ContentType.objects.get_for_model(modelo)
                for accion in acciones:
                    permisos.append(Permission.objects.get(content_type=ct, codename=f"{accion}_{modelo._meta.model_name}"))
            grupo.permissions.set(permisos)
            self.stdout.write(self.style.SUCCESS(f"Grupo «{nombre}»: {len(permisos)} permisos"))

        for username, grupo, var, default in USUARIOS:
            user, _ = User.objects.get_or_create(username=username)
            user.is_staff = True  # necesario para entrar a /admin (los permisos los dicta el grupo)
            user.set_password(os.getenv(var, default))
            user.save()
            user.groups.set([Group.objects.get(name=grupo)])
            self.stdout.write(self.style.SUCCESS(f"Usuario «{username}» -> {grupo}"))
