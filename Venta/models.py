from django.db import models
from Inventario.models import Producto
# Create your models here.

class Venta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha_venta = models.DateTimeField(auto_now_add=True)
