from django.urls import path
from .views import ImportarProductosView

urlpatterns = [
    path('importar_productos/', ImportarProductosView.as_view(), name='importar_productos'),
]