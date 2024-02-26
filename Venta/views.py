from django.shortcuts import render, redirect
from django.views import View
from .models import Venta
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import VentaForm 
from Inventario.models import Producto
from django.db.models import Q

from django.shortcuts import render, redirect


class BuscadorProductosMixin:
    def buscar(self):
        busqueda = self.request.GET.get("Buscar")
        self.productos = Producto.objects.all()

        if busqueda:
            atributos_a_buscar = ['nombre', 'medida', 'codigo_barras','codigo_producto', 'existencia','precio_venta','precio_compra']
            query = Q()

            for atributo in atributos_a_buscar:
                query |= Q(**{f'{atributo}__icontains': busqueda})

            self.productos = self.productos.filter(query)

    def get_context_data(self, **kwargs):
        self.buscar()
        context = super().get_context_data(**kwargs)
        context['Productos'] = self.productos
        return context

class ProductoListView(BuscadorProductosMixin, ListView):
    model = Producto
    template_name = 'ver_productos_venta.html'
    context_object_name = 'Productos'

class AgregarAlCarritoView(View):
    template_name = 'venta/agregar_al_carrito.html'

    def get(self, request, *args, **kwargs):
        form = VentaForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = VentaForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']

            # Lógica para agregar al carrito (puedes usar sesiones para almacenar el carrito)
            carrito = request.session.get('carrito', [])
            carrito.append({'producto': producto.id, 'cantidad': cantidad})
            request.session['carrito'] = carrito

            return redirect('ver_carrito')

        return render(request, self.template_name, {'form': form})


class VentaView(View):
    template_name = 'venta.html'
    form_class = VentaForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['elemento']
            cantidad = form.cleaned_data['cantidad']

            # Obtener el precio de venta del producto
            precio_venta = producto.precio_venta

            # Calcular el total de la venta
            total_venta = cantidad * precio_venta

            # Crear y guardar la venta
            venta = Venta(producto=producto, cantidad=cantidad, precio_unitario=precio_venta, total_venta=total_venta)
            venta.save()

            # Lógica adicional para generar el ticket
            # ...

            return render(request, 'venta_confirmacion.html', {'total_venta': total_venta})

        return render(request, self.template_name, {'form': form})
