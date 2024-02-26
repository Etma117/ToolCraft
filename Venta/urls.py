# En tu aplicación venta/urls.py

from django.urls import path
from .views import VentaView, ProductoListView


urlpatterns = [
    path('venta/', ProductoListView.as_view(), name='venta_productos'),
]
