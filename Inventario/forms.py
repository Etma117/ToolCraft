from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        
        labels = {
            'nombre': 'Nombre del Producto',
            'medida': 'Medida (por ejemplo: cm, pulg, kg, oz o litros)',
            'codigo_barras': 'Código de Barras',
            'codigo_producto': 'Código del Producto',
            'existencia': 'Existencias Disponibles',
            'precio_venta': 'Precio de Venta',
            'precio_compra': 'Precio de Compra',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'medida': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'existencia': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control'}),
        }