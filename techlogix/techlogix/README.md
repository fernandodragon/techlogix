# TechLogix S.A. — Sistema de catálogo e inventario (Django + PostgreSQL)

Evaluación Sumativa 02 · Backend · Unidad 2

Aplicación web en Django que gestiona el catálogo e inventario de productos de TechLogix S.A. sobre PostgreSQL, con login y dos perfiles (Administrador y Asistente).

## Requisitos
- Python 3.10+ y PostgreSQL 14+

## Instalación paso a paso

```bash
# 1. Entorno virtual
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Crear la base de datos en PostgreSQL (psql como superusuario)
#    CREATE USER techlogix_user WITH PASSWORD 'tu_clave';
#    CREATE DATABASE techlogix_db OWNER techlogix_user;

# 3. Variables de entorno
cp .env.example .env            # Windows: copy .env.example .env
#    Edita .env con tus credenciales reales y una DJANGO_SECRET_KEY propia

# 4. Migraciones
python manage.py makemigrations   # debe decir "No changes detected"
python manage.py migrate

# 5. Grupos, permisos y usuarios de prueba + datos de ejemplo
python manage.py setup_roles
python manage.py seed_datos

# 6. Ejecutar
python manage.py runserver
```

Pruebas automáticas (verifican los permisos por rol): `python manage.py test`

## Usuarios de prueba

| Perfil | Usuario | Contraseña | Permisos |
|---|---|---|---|
| Administrador | `admin_tech` | `Admin_Tech_2026` | Crear, Leer, Actualizar y Eliminar |
| Asistente | `asistente_tech` | `Asist_Tech_2026` | Solo lectura |

(Las contraseñas pueden cambiarse con `ADMIN_TECH_PASSWORD` y `ASISTENTE_TECH_PASSWORD` en `.env` antes de ejecutar `setup_roles`.)

## Rutas

| URL | Template | Acceso |
|---|---|---|
| `/` | `index.html` | Público |
| `/catalogo/` | `catalogo.html` (filtro por categoría y búsqueda por nombre) | Público |
| `/login/` | `login.html` | Público |
| `/gestion/` | `admin_panel.html` (tabla del catálogo interno) | Autenticado (permiso `view`) |
| `/gestion/producto/<id>/` | `producto_detail.html` | Autenticado (permiso `view`) |
| `/gestion/producto/nuevo/` | `producto_form.html` | Solo Administrador (`add`) |
| `/gestion/producto/<id>/editar/` | `producto_form.html` | Solo Administrador (`change`) |
| `/gestion/producto/<id>/eliminar/` | `producto_confirm_delete.html` (pide confirmación) | Solo Administrador (`delete`) |
| `/admin/` | Admin nativo de Django | Staff según permisos del grupo |

## Cómo se cumple cada criterio

- **2.1.1 BD:** `settings.py` usa `django.db.backends.postgresql` y lee `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` desde `.env` (excluido por `.gitignore`). Se incluye la migración `inventario/migrations/0001_initial.py`.
- **2.1.2 Admin:** `Categoria` y `Producto` registrados; `Producto` con `list_display`, `list_filter` y `search_fields`. El comando `setup_roles` crea los grupos *Administrador* (add/change/delete/view) y *Asistente* (solo view) sobre ambos modelos.
- **2.1.3 CRUD:** vistas basadas en clases (`CreateView`, `ListView`/`DetailView`, `UpdateView`, `DeleteView` con página de confirmación) en `inventario/views.py`.
- **2.1.4 Seguridad:** `PermisoRequeridoMixin` (login + permiso) en todas las vistas privadas: un Asistente que intente crear/editar/eliminar recibe **403** en el backend; además los botones se ocultan con `{% if perms.inventario.* %}`. Todos los formularios incluyen `{% csrf_token %}` (el cierre de sesión también es POST).

## Registro de uso de IA (prompts)

> Completa/ajusta esta tabla con los prompts que realmente utilizaste.

| # | Herramienta | Prompt utilizado | Para qué se usó | Resultado / ajuste |
|---|---|---|---|---|
| 1 | Claude | Se entregó la pauta de la evaluación (caso TechLogix S.A.) y la rúbrica, pidiendo construir el proyecto Django completo (settings con PostgreSQL y .env, modelos Categoria/Producto, admin personalizado, CRUD, 3 templates, login, roles Administrador/Asistente y README). | Generar la estructura base del proyecto, vistas con mixins de permisos y templates. | Se revisó el código, se creó la BD local y se ejecutaron migraciones y `manage.py test`. |
| 2 | (ej. Claude/ChatGPT) | *«Me aparece el error `FATAL: password authentication failed for user` al hacer migrate en Django con PostgreSQL, ¿qué reviso?»* | Depurar la conexión a PostgreSQL. | *(describe qué corregiste)* |
| 3 | (ej. Claude/ChatGPT) | *«Genera 15 productos de prueba de tecnología con SKU, precio y stock para cargar en Django»* | Datos de prueba (`seed_datos`). | *(describe qué ajustaste)* |
