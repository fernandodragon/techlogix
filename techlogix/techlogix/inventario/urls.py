from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("catalogo/", views.CatalogoView.as_view(), name="catalogo"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("gestion/", views.PanelView.as_view(), name="admin_panel"),
    path("gestion/producto/nuevo/", views.ProductoCreateView.as_view(), name="producto_crear"),
    path("gestion/producto/<int:pk>/", views.ProductoDetailView.as_view(), name="producto_detalle"),
    path("gestion/producto/<int:pk>/editar/", views.ProductoUpdateView.as_view(), name="producto_editar"),
    path("gestion/producto/<int:pk>/eliminar/", views.ProductoDeleteView.as_view(), name="producto_eliminar"),
]
