from django.db import models
from django.contrib.auth.models import User
from Inventario.models import Producto

class VentaModel(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2)
    total_invertido = models.DecimalField(max_digits=10, decimal_places=2, null= True, default=0)
    ganancia=models.DecimalField(max_digits=10,decimal_places=2,null=True, default=0)  

    fecha_venta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Venta{self.id}-{self.fecha_venta}'

class DetalleVenta(models.Model):
    # Relación con el producto (no se elimina si el producto se elimina)
    producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)

    # Campos adicionales para nombre y medida del producto
    nombre_producto = models.CharField(max_length=255, default="Producto")
    medida_producto = models.CharField(max_length=50, null=True, blank=True)

    # Otros campos de detalle de venta
    venta = models.ForeignKey(VentaModel, related_name='detalle', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Detalle {self.id} - {self.nombre_producto} - {self.venta}'