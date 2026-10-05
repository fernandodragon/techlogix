from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import ProductoForm
from .mixins import PermisoRequeridoMixin
from .models import Categoria, Producto


def filtrar(queryset, request):
    """Búsqueda por nombre (?q=) y filtro por categoría (?categoria=)."""
    q = request.GET.get("q", "").strip()
    categoria = request.GET.get("categoria", "")
    if q:
        queryset = queryset.filter(nombre__icontains=q)
    if categoria.isdigit():
        queryset = queryset.filter(categoria_id=int(categoria))
    return queryset


class ListadoBase(ListView):
    model = Producto
    paginate_by = 10
    context_object_name = "productos"

    def get_queryset(self):
        return filtrar(Producto.objects.select_related("categoria"), self.request)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        params = self.request.GET.copy()
        params.pop("page", None)
        ctx.update(
            categorias=Categoria.objects.all(),
            q=self.request.GET.get("q", ""),
            categoria_sel=self.request.GET.get("categoria", ""),
            querystring=params.urlencode(),
        )
        return ctx


# ---------- Públicas ----------
class IndexView(TemplateView):
    template_name = "index.html"


class CatalogoView(ListadoBase):
    template_name = "catalogo.html"


# ---------- Privadas (CRUD) ----------
class PanelView(PermisoRequeridoMixin, ListadoBase):  # READ (listado)
    permission_required = "inventario.view_producto"
    template_name = "admin_panel.html"


class ProductoDetailView(PermisoRequeridoMixin, DetailView):  # READ (detalle)
    permission_required = "inventario.view_producto"
    model = Producto


class ProductoCreateView(PermisoRequeridoMixin, SuccessMessageMixin, CreateView):  # CREATE
    permission_required = "inventario.add_producto"
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy("admin_panel")
    success_message = "Producto creado correctamente."


class ProductoUpdateView(PermisoRequeridoMixin, SuccessMessageMixin, UpdateView):  # UPDATE
    permission_required = "inventario.change_producto"
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy("admin_panel")
    success_message = "Producto actualizado correctamente."


class ProductoDeleteView(PermisoRequeridoMixin, DeleteView):  # DELETE (con página de confirmación)
    permission_required = "inventario.delete_producto"
    model = Producto
    success_url = reverse_lazy("admin_panel")

    def form_valid(self, form):
        messages.success(self.request, f"Producto «{self.object.nombre}» eliminado.")
        return super().form_valid(form)
