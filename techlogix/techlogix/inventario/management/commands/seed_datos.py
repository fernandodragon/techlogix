"""Carga categorías y productos de prueba.  Uso:  python manage.py seed_datos"""
from decimal import Decimal

from django.core.management.base import BaseCommand

from inventario.models import Categoria, Producto

DATOS = {
    "Notebooks": ("Equipos portátiles", [("Notebook Lenovo ThinkPad E14", "NB-LEN-E14", 649990, 12), ("Notebook HP ProBook 450", "NB-HP-450", 589990, 8), ("Notebook ASUS Vivobook 15", "NB-ASU-V15", 459990, 15)]),
    "Periféricos": ("Teclados, mouses y accesorios", [("Mouse Logitech MX Master 3S", "PE-LOG-MX3S", 99990, 25), ("Teclado mecánico Redragon K552", "PE-RED-K552", 39990, 30), ("Webcam Logitech C920", "PE-LOG-C920", 74990, 14)]),
    "Redes": ("Equipamiento de conectividad", [("Router TP-Link Archer AX55", "RE-TPL-AX55", 89990, 18), ("Switch Gigabit 8 puertos", "RE-SW-8G", 24990, 40), ("Access Point Ubiquiti U6 Lite", "RE-UBI-U6L", 119990, 9)]),
    "Almacenamiento": ("Discos y memorias", [("SSD NVMe 1TB Kingston NV2", "AL-KIN-1TB", 62990, 35), ("Disco externo WD 2TB", "AL-WD-2TB", 79990, 20), ("Pendrive 128GB SanDisk", "AL-SAN-128", 12990, 60)]),
    "Monitores": ("Pantallas y accesorios", [("Monitor LG 24'' IPS", "MO-LG-24", 129990, 11), ("Monitor Samsung 27'' Curvo", "MO-SAM-27C", 189990, 7)]),
}


class Command(BaseCommand):
    help = "Carga datos de prueba (idempotente)."

    def handle(self, *args, **options):
        total = 0
        for nombre, (desc, productos) in DATOS.items():
            cat, _ = Categoria.objects.get_or_create(nombre=nombre, defaults={"descripcion": desc})
            for pn, sku, precio, stock in productos:
                _, creado = Producto.objects.get_or_create(sku=sku, defaults={"nombre": pn, "categoria": cat, "precio": Decimal(precio), "stock": stock})
                total += creado
        self.stdout.write(self.style.SUCCESS(f"{total} productos nuevos cargados."))
