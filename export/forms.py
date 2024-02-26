from django import forms


class ImportarProductosForm(forms.Form):
    file = forms.FileField()
