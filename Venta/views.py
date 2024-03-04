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
from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth


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

    # Verificar si hay productos en la venta antes de proceder
    if not venta.venta:
        return render(request, 'venta_realizada.html', {'mensaje': 'La venta está vacía.'})

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

    return render(request, 'venta_realizada.html', {'venta': nueva_venta})



def todas_las_ventas(request):
    ventas = VentaModel.objects.all()
    ventas_detalles = [venta.detalle.all() for venta in ventas]
    context = {'ventas': ventas, 'ventas_detalles': ventas_detalles}
    
    return render(request, 'todas_las_ventas.html', context)


def ventas_por_dia(request, fecha_seleccionada):
    # Convierte la fecha de cadena a objeto datetime si es necesario
    # La fecha_seleccionada debe estar en formato 'YYYY-MM-DD'
    from datetime import datetime
    fecha_objeto = datetime.strptime(fecha_seleccionada, '%Y-%m-%d').date()

    # Obtén las ventas para la fecha seleccionada
    ventas_del_dia = VentaModel.objects.filter(fecha_venta__date=fecha_objeto)

    total_ventas = ventas_del_dia.aggregate(Sum('total'))['total__sum'] or 0

    context = {
        'fecha_seleccionada': fecha_seleccionada,
        'ventas_del_dia': ventas_del_dia,
        'total_ventas': total_ventas,
    }

    return render(request, 'ventas_por_dia.html', context)

def reporte_ventas_por_semana(request):
    ventas_por_semana = VentaModel.objects.annotate(semana=TruncWeek('fecha_venta')).values('semana').annotate(total_semana=Sum('total'))
    return render(request, 'reporte_ventas_por_semana.html', {'ventas_por_semana': ventas_por_semana})

def reporte_ventas_por_mes(request):
    ventas_por_mes = VentaModel.objects.annotate(mes=TruncMonth('fecha_venta')).values('mes').annotate(total_mes=Sum('total'))
    return render(request, 'reporte_ventas_por_mes.html', {'ventas_por_mes': ventas_por_mes})


    

