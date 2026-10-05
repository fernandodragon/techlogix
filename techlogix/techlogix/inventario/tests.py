from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Producto


class PermisosPorRolTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("setup_roles", verbosity=0)
        cat = Categoria.objects.create(nombre="Redes")
        cls.producto = Producto.objects.create(nombre="Router", categoria=cat, precio=10000, stock=5, sku="RT-1")

    def test_anonimo_es_redirigido_al_login(self):
        r = self.client.get(reverse("admin_panel"))
        self.assertEqual(r.status_code, 302)
        self.assertIn(reverse("login"), r.url)

    def test_paginas_publicas(self):
        self.assertEqual(self.client.get(reverse("index")).status_code, 200)
        self.assertEqual(self.client.get(reverse("catalogo")).status_code, 200)

    def test_asistente_solo_lectura(self):
        self.client.login(username="asistente_tech", password="Asist_Tech_2026")
        self.assertEqual(self.client.get(reverse("admin_panel")).status_code, 200)
        self.assertEqual(self.client.get(reverse("producto_detalle", args=[self.producto.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("producto_crear")).status_code, 403)
        self.assertEqual(self.client.post(reverse("producto_editar", args=[self.producto.pk]), {}).status_code, 403)
        self.assertEqual(self.client.post(reverse("producto_eliminar", args=[self.producto.pk])).status_code, 403)
        self.assertTrue(Producto.objects.filter(pk=self.producto.pk).exists())

    def test_administrador_crud_completo(self):
        self.client.login(username="admin_tech", password="Admin_Tech_2026")
        datos = {"nombre": "Switch", "categoria": self.producto.categoria_id, "precio": "5000", "stock": 3, "sku": "sw-1", "fecha_ingreso": "2026-10-05"}
        self.assertEqual(self.client.post(reverse("producto_crear"), datos).status_code, 302)
        nuevo = Producto.objects.get(sku="SW-1")
        datos["stock"] = 9
        self.client.post(reverse("producto_editar", args=[nuevo.pk]), datos)
        nuevo.refresh_from_db()
        self.assertEqual(nuevo.stock, 9)
        self.client.post(reverse("producto_eliminar", args=[nuevo.pk]))
        self.assertFalse(Producto.objects.filter(pk=nuevo.pk).exists())
