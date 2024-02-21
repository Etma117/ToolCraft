from django.db import models

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre del Producto')
    medida = models.CharField(max_length=255, verbose_name='Medida (por ejemplo: cm, pulg, kg, oz o litros)', blank=True, null=True,)
    codigo_barras = models.CharField(max_length=255, verbose_name="Codigo de Barra", blank=True, null=True,)
    codigo_producto = models.CharField(blank=True, null=True, unique= True, max_length=25, verbose_name='Codigo Producto')
    
    existencia = models.PositiveIntegerField(verbose_name='Existencias Disponible', blank=True, null=True,)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio de Venta', blank=True, null=True,)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio de Compra', blank=True, null=True,)
    
    fecha_creacion = models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')
    
    imagen = models.ImageField(blank=True, null=True, verbose_name='Imagen del Producto')


    # NOMBRE 	MEDIDA	CODIGO DE BARRA	CODIGO/PRODUCTO 	EXISTENCIA 	 PRECIO/VENTA 	 PRECIO/COMPRA  


    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Productos'