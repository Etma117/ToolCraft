# En tu aplicación venta/urls.py

from django.urls import path
from .views import  ProductoListView, agregar_producto, agregar_varios_productos ,agregar_otro, restar_producto, ver_venta, eliminar_producto, realizar_compra, limpiar_venta

from .views import todas_las_ventas, ventas_por_dia, ventas_por_semana, enviarSemana, ventas_por_mes

urlpatterns = [
    path('nueva-venta/', ProductoListView.as_view(), name='venta_productos'),
    
    path('agregar/<int:producto_id>/', agregar_producto, name="Agregar"), 
    path('agregar_varios_productos/<int:producto_id>/', agregar_varios_productos, name="Agregar_varios"), 
    path('agregar_otro/<int:producto_id>/', agregar_otro, name="AgregarMas"),
    path('restar_producto/<int:producto_id>/', restar_producto, name="restar_producto"),   
    path('eliminar_producto/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('ver_venta/', ver_venta, name='ver_venta'),
    path('realizar_compra/', realizar_compra, name='realizar_compra'),

    path('limpiar_venta/', limpiar_venta, name='eliminar_todos'),


    path('todas-las-ventas/', todas_las_ventas, name='todas_las_ventas'),
    path('ventas_por_dia/<str:fecha_seleccionada>/', ventas_por_dia, name='ventas_por_dia'),
    path('ventas_por_semana/<int:ano>/<int:numero_semana>/', ventas_por_semana, name='ventas_por_semana'),
    path('enviar-semana/', enviarSemana, name='enviar_semana'),
    path('ventas_por_mes/', ventas_por_mes, name='ventas_por_mes'),

    

]
