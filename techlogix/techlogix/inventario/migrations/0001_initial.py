import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Categoria",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=100, unique=True)),
                ("descripcion", models.TextField(blank=True)),
            ],
            options={"verbose_name_plural": "categorías", "ordering": ["nombre"]},
        ),
        migrations.CreateModel(
            name="Producto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=150)),
                ("precio", models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ("stock", models.PositiveIntegerField(default=0)),
                ("sku", models.CharField(max_length=50, unique=True)),
                ("fecha_ingreso", models.DateField(default=django.utils.timezone.localdate)),
                ("categoria", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="productos", to="inventario.categoria")),
            ],
            options={"ordering": ["nombre"]},
        ),
    ]
