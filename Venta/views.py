from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Q

from .forms import VentaForm 
from Inventario.models import Producto
from .models import VentaModel
from .venta import Venta

from .context_processor import total_venta

from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from datetime import datetime, timedelta, date
from django.urls import reverse
from django.http import HttpResponseRedirect


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
        context['object_list'] = self.productos
        return context

class ProductoListView(BuscadorProductosMixin, ListView):
    model = Producto
    template_name = 'ver_productos_venta.html'
    context_object_name = 'Productos'
    paginate_by = 32
    queryset = Producto.objects.order_by("nombre")

   

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
    total_venta_invertido = sum(value['acumulado_compra'] for key, value in venta.venta.items())

    # Crear un objeto de venta en la base de datos
    nueva_venta = VentaModel(
        total=total_venta,
        total_invertido = total_venta_invertido,
        ganancia= total_venta - total_venta_invertido
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
    
    fecha_objeto = datetime.strptime(fecha_seleccionada, '%Y-%m-%d').date()

    # Obtén las ventas para la fecha seleccionada
    ventas_del_dia = VentaModel.objects.filter(fecha_venta__date=fecha_objeto)

    total_ventas = ventas_del_dia.aggregate(Sum('total'))['total__sum'] or 0
    total_invertido = ventas_del_dia.aggregate(Sum('total_invertido'))['total_invertido__sum'] or 0
    total_ganancia = ventas_del_dia.aggregate(Sum('ganancia'))['ganancia__sum'] or 0

    context = {
        'fecha_seleccionada': fecha_seleccionada,
        'ventas_del_dia': ventas_del_dia,
        'total_ventas': total_ventas,
        'total_invertido': total_invertido,
        'total_ganancia': total_ganancia,
    }

    return render(request, 'ventas_por_dia.html', context)

def ventas_por_semana(request, ano, numero_semana):
    # Calcula la fecha de inicio y fin de la semana
    inicio_semana = date.fromisocalendar(ano, numero_semana, 1)
    fin_semana = inicio_semana + timedelta(days=6)

    # Obtén las ventas para la semana seleccionada
    ventas_de_la_semana = VentaModel.objects.filter(fecha_venta__range=[inicio_semana, fin_semana])

    total_ventas = ventas_de_la_semana.aggregate(Sum('total'))['total__sum'] or 0
    total_invertido = ventas_de_la_semana.aggregate(Sum('total_invertido'))['total_invertido__sum'] or 0
    total_ganancia = ventas_de_la_semana.aggregate(Sum('ganancia'))['ganancia__sum'] or 0

    context = {
        'ano': ano,
        'numero_semana': numero_semana,
        'ventas_de_la_semana': ventas_de_la_semana,
        'total_ventas': total_ventas,
        'total_invertido': total_invertido,
        'total_ganancia': total_ganancia,
    }

    return render(request, 'ventas_por_semana.html', context)

def enviarSemana(request):
    ano = request.GET.get('ano', '')
    semana = request.GET.get('semana', '')

    # Construir la URL utilizando reverse
    url = reverse('ventas_por_semana', kwargs={'ano': ano, 'numero_semana': semana})

    return HttpResponseRedirect(url)

def reporte_ventas_por_mes(request):
    ventas_por_mes = VentaModel.objects.annotate(mes=TruncMonth('fecha_venta')).values('mes').annotate(total_mes=Sum('total'))
    return render(request, 'reporte_ventas_por_mes.html', {'ventas_por_mes': ventas_por_mes})


    

