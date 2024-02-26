from django import forms
from Inventario.models import Producto

class VentaForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all())
    cantidad = forms.IntegerField(min_value=1, widget=forms.TextInput(attrs={'class': 'cantidad-input'}))

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor que cero.")
        return cantidad
