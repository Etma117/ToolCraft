from django.shortcuts import render, redirect
from django.views import View
from .venta import Venta
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import VentaForm 
from Inventario.models import Producto
from .models import VentaModel

from .context_processor import total_venta
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

def agregar_otro(request, producto_id):
    venta = Venta(request)
    producto = Producto.objects.get(id=producto_id)
    venta.agregar(producto)
    
    return redirect("ver_venta")

def restar_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    venta = Venta(request)
    venta.restar(producto)
    return redirect('ver_venta')

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
    total_venta = sum(value['acumulado'] for key, value in venta.venta.items())

    # Crear un objeto de venta en la base de datos
    nueva_venta = VentaModel(
        total=total_venta
    )
    nueva_venta.save()

    # Iterar sobre los productos vendidos y relacionarlos con la venta
    for key, value in venta.venta.items():
        producto = Producto.objects.get(id=value['producto_id'])
        nueva_venta.detalle.create(
            producto=producto,
            cantidad=value['cantidad'],
            precio_unitario=value['precio_venta'],
            total=value['acumulado']
        )

        
    # Limpiar carrito después de la compra
    venta.limpiar()

    return render(request, 'compra_realizada.html')

