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


class MesAnoForm(forms.Form):
    MESES = [
        (1, 'Enero'), (2, 'Febrero'), (3, 'Marzo'), (4, 'Abril'),
        (5, 'Mayo'), (6, 'Junio'), (7, 'Julio'), (8, 'Agosto'),
        (9, 'Septiembre'), (10, 'Octubre'), (11, 'Noviembre'), (12, 'Diciembre')
    ]

    ANOS = [(year, str(year)) for year in range(2024, 2034)]

    mes = forms.ChoiceField(
        choices=MESES,
        label='Mes',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    ano = forms.ChoiceField(
        choices=ANOS,
        label='Año',
        widget=forms.Select(attrs={'class': 'form-control'})
    )