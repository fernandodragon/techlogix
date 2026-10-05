## Uso de Inteligencia Artificial

Herramienta utilizada: Claude (Anthropic, modelo Sonnet 5.5), apoyo para planificación, configuración y depuración.

| N° | Prompt utilizado | Para qué se usó |
|----|------------------|-----------------|
| 1 | "¿Qué hago ahora?" (adjuntando el enunciado de la evaluación en .docx y una captura de VS Code con Django recién instalado) | Obtener un plan de trabajo ordenado según los criterios de la rúbrica |
| 2 | "El proyecto es sin entorno virtual" | Ajustar la entrega: cómo armar `requirements.txt` y qué excluir del repositorio |
| 3 | "Dame un paso a paso de cómo hacerlo desde el principio con las instrucciones que te di" | Guía completa: configuración de PostgreSQL y `settings.py` con `.env`, modelos, admin, grupos y permisos, vistas CRUD, templates y pruebas |
| 4 | "¿Qué pongo acá?" (captura del asistente Stack Builder al terminar de instalar PostgreSQL) | Resolver una duda durante la instalación de PostgreSQL |
| 5 | Captura del error "no se encontró Python; ejecutar sin argumentos para instalar desde el Microsoft Store" | Resolver el alias de la Microsoft Store y usar el lanzador `py` |
| 6 | Traceback `Falta la variable de entorno DJANGO_SECRET_KEY` | Detectar que el `.env` no estaba guardado y ordenar `settings.py` (imports duplicados, uso de `env()`) |
| 7 | Error `la autenticación password falló para el usuario postgres` | Corregir `DB_PASSWORD` en el `.env` y ejecutar las migraciones sin errores |

### Cómo se usó el resultado

- La IA propuso el código base del `settings.py` con variables de entorno, los modelos `Categoria` y `Producto`, el `admin.py` personalizado, los comandos `setup_roles` (grupos Administrador y Asistente) y `seed_datos` (datos de ejemplo), las vistas CRUD con `LoginRequiredMixin` y `PermissionRequiredMixin`, y los templates.
- El código fue revisado, probado y ajustado por mí en mi entorno local.
