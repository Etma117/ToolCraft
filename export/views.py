from django.shortcuts import render

from django.views.generic import ListView, TemplateView, View
from django.http import HttpResponseRedirect
from .forms import ImportarProductosForm
from .admin import ProductoResource
from tablib import Dataset
import pandas as pd
import io  # Agrega esta importación

class ImportarProductosView(View):
    template_name = 'importar_productos.html'

    def get(self, request):
        form = ImportarProductosForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ImportarProductosForm(request.POST, request.FILES)
        if form.is_valid():
            file_format = 'xlsx'
            resource = ProductoResource()

            # Utiliza io.BytesIO para envolver los bytes
            xls_file = pd.ExcelFile(io.BytesIO(request.FILES['file'].read()), engine='openpyxl')

            for sheet_name in xls_file.sheet_names:
                dataset = Dataset()
                df = xls_file.parse(sheet_name)
                dataset.dict = df.to_dict(orient='records')

                result = resource.import_data(dataset, dry_run=True, raise_errors=False)

                if not result.has_errors():
                    resource.import_data(dataset, dry_run=False, raise_errors=True)

            return HttpResponseRedirect('/productos')  # Redirige a la página deseada después de la importación

        return render(request, self.template_name, {'form': form})
