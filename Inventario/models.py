from django.db import models

# Create your models here.
class Producto(models.Model):
    nombre = models.CharField(max_length=255, verbose_name='Nombre del Producto')
    marca = models.CharField(max_length=255, verbose_name="Marca")
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción del Producto')

    medida = models.CharField(max_length=255, verbose_name='Medida (por ejemplo: cm, pulg, kg, oz o litros)', blank=True)
    codigo_producto = models.CharField(blank=True, null=True, unique= True, max_length=25)
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    stock = models.PositiveIntegerField(verbose_name='Stock Disponible')
    fecha_creacion = models.DateField(auto_now_add=True, verbose_name='Fecha de Creación')
    
    imagen = models.ImageField(blank=True, null=True, verbose_name='Imagen del Producto')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = 'Productos'