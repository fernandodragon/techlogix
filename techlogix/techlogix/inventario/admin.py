from django.contrib import admin
from django.db.models import Count

from .models import Categoria, Producto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion", "total_productos")
    search_fields = ("nombre", "descripcion")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_total=Count("productos"))

    @admin.display(description="Productos", ordering="_total")
    def total_productos(self, obj):
        return obj._total


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "sku", "categoria", "precio", "stock", "fecha_ingreso")
    list_filter = ("categoria", "fecha_ingreso")
    search_fields = ("nombre", "sku", "categoria__nombre")
    list_select_related = ("categoria",)
    date_hierarchy = "fecha_ingreso"
    ordering = ("nombre",)
