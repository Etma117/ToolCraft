# En tu aplicación venta/urls.py

from django.urls import path
from .views import  ProductoListView, agregar_producto, ver_venta, eliminar_producto



urlpatterns = [
    path('nueva-venta/', ProductoListView.as_view(), name='venta_productos'),
    path('agregar/<int:producto_id>/', agregar_producto, name="Agregar"),    
    path('eliminar_producto/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('ver_venta/', ver_venta, name='ver_venta'),
    

]
