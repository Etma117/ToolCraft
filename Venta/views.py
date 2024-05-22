from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.db.models import Q
from django.contrib import messages

from .forms import VentaForm, MesAnoForm
from Inventario.models import Producto
from .models import VentaModel
from .venta import Venta

from .context_processor import total_venta

from django.db.models import Sum
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from datetime import datetime, timedelta, date
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin


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

class ProductoListView(LoginRequiredMixin, BuscadorProductosMixin, ListView):

    login_url = 'login'  # URL de inicio de sesión
    redirect_field_name = 'next'  # Nombre del campo de redireccionamiento

    model = Producto
    template_name = 'ver_productos_venta.html'
    context_object_name = 'Productos'
    paginate_by = 32
    queryset = Producto.objects.order_by("nombre")

  
def agregar_producto(request, producto_id):
    venta = Venta(request)
    try:
        producto = Producto.objects.get(id=producto_id)
        if producto.existencia > 0:
            venta.agregar(producto)

            # Reduce las existencias del producto
            producto.existencia -= 1
            producto.save()

            if producto.existencia <= 3:
                if  producto.existencia ==0:
                    messages.warning(request, f"No quedan existencias del producto {producto.nombre} de {producto.medida}")
                else:
                    messages.warning(request, f"Solo quedan {producto.existencia} existencias del producto {producto.nombre} de {producto.medida}")

            # Agrega un mensaje
            messages.success(request, f"Producto {producto.nombre} de {producto.medida} agregado a la venta.")
        else:
            messages.error(request, f"Lo sentimos, el producto {producto.nombre} de {producto.medida} no está disponible en este momento. Sin existencias")
    except Producto.DoesNotExist:
        messages.error(request, "El producto solicitado no existe.")
    return redirect("venta_productos")

def agregar_otro(request, producto_id):
    venta = Venta(request)
    try:
        producto = Producto.objects.get(id=producto_id)
        if producto.existencia > 0:
            venta.agregar(producto)

            # Reduce las existencias del producto
            producto.existencia -= 1
            producto.save()

            if producto.existencia <= 3:
                messages.warning(request, f"Solo quedan {producto.existencia} existencias del producto {producto.nombre} de {producto.medida}")

            # Agrega un mensaje
            messages.success(request, f"Producto {producto.nombre} de {producto.medida} agregado a la venta.")
        else:
            messages.warning(request, f"Lo sentimos, el producto {producto.nombre} de {producto.medida} no está disponible en este momento.")
    except Producto.DoesNotExist:
        messages.error(request, "El producto solicitado no existe.")
    return redirect("ver_venta")

def restar_producto(request, producto_id):
    producto = Producto.objects.get(id=producto_id)
    venta = Venta(request)
    venta.restar(producto)

    # Incrementa las existencias del producto
    producto.existencia += 1
    producto.save()

    messages.warning(request, f"Removido una unidad del Producto {producto.nombre} de {producto.medida} de la venta.")

    return redirect('ver_venta')

def eliminar_producto(request, producto_id):
    venta = Venta(request)
    producto = Producto.objects.get(id=producto_id)
    venta.eliminar(producto)

    messages.error(request, f"Producto {producto.nombre} de {producto.medida} completamente removido de la venta.")

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
    
    if request.method == 'POST':
        form = MesAnoForm(request.POST)
        if form.is_valid():
            # Procesar el formulario y redirigir a la página de ventas del mes
            mes = form.cleaned_data['mes']
            ano = form.cleaned_data['ano']
            
            # Puedes redirigir a la vista por mes con los datos del formulario
            return HttpResponseRedirect(f'/ventas-por-mes/{ano}/{mes}/')
    else:
        form = MesAnoForm()

    context = {'ventas': ventas, 'ventas_detalles': ventas_detalles, 'form': form}
    
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
    # Obtén la fecha desde el formulario del HTML (asegúrate de que sea un formato adecuado)
    fecha_seleccionada_str = request.GET.get('fecha_seleccionada', '')
    
    # Convierte la cadena a un objeto de fecha
    fecha_seleccionada = datetime.strptime(fecha_seleccionada_str, '%Y-%m-%d').date()

    # Obtén el número de semana y el año para la fecha seleccionada
    numero_semana = fecha_seleccionada.isocalendar()[1]
    ano_semana = fecha_seleccionada.year

    # Construir la URL utilizando reverse
    url = reverse('ventas_por_semana', kwargs={'ano': ano_semana, 'numero_semana': numero_semana})

    return HttpResponseRedirect(url)

def ventas_por_mes(request):
    if request.method == 'POST':
        form = MesAnoForm(request.POST)
        if form.is_valid():
            ano = form.cleaned_data['ano']
            mes = form.cleaned_data['mes']
            
            # Lógica para obtener las ventas del mes
            # Ajusta esto según tus modelos y lógica específica
            ventas_del_mes = VentaModel.objects.filter(fecha_venta__year=ano, fecha_venta__month=mes)
            
            total_ventas = ventas_del_mes.aggregate(Sum('total'))['total__sum'] or 0
            total_invertido = ventas_del_mes.aggregate(Sum('total_invertido'))['total_invertido__sum'] or 0
            total_ganancia = ventas_del_mes.aggregate(Sum('ganancia'))['ganancia__sum'] or 0

            context = {
                'ano': ano,
                'mes': mes,
                'ventas_del_mes': ventas_del_mes,
                'total_ventas': total_ventas,
                'total_invertido': total_invertido,
                'total_ganancia': total_ganancia,
            }

            return render(request, 'ventas_por_mes.html', context)
    else:
        form = MesAnoForm()

    return render(request, 'ventas_por_mes_form.html', {'form': form})

