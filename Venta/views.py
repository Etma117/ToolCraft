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

def agregar_producto(request, producto_id):
    venta = Venta(request)
    producto = Producto.objects.get(id=producto_id)
    venta.agregar(producto)
    
    return redirect("venta_productos")

def eliminar_producto(request, producto_id):
    venta = Venta(request)
    producto = Producto.objects.get(id=producto_id)
    venta.eliminar(producto)
    return redirect('ver_venta')

def ver_venta(request):
    venta = Venta(request)
    carrito = venta.venta   
    return render(request, 'ver_venta.html', {'carrito': carrito})

def realizar_compra(request):
    venta = Venta(request)
    # Lógica para procesar la compra y actualizar modelos
    venta.limpiar()
    return render(request, 'compra_realizada.html')

