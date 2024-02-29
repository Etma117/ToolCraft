from django.contrib import admin

from .models import VentaModel, DetalleVenta

# Register your models here.

admin.site.register(VentaModel)

admin.site.register(DetalleVenta)