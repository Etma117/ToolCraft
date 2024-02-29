from django.db import models
from django.contrib.auth.models import User
from Inventario.models import Producto

class VentaModel(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_venta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Venta{self.id}-{self.fecha_venta}'

class DetalleVenta(models.Model):
    venta = models.ForeignKey(VentaModel, related_name='detalle', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Detalle {self.id} - {self.producto.nombre} - {self.venta}'

