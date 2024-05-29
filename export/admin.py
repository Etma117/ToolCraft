from django.contrib import admin

# Register your models here.
from import_export import resources
from import_export.admin import ImportMixin
from Inventario.models import Producto

from .resources import ProductoResource

class ProductoAdmin(ImportMixin, admin.ModelAdmin):
    resource_classes = [ProductoResource]

admin.site.register(Producto, ProductoAdmin)

