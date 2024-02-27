from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Producto
from .forms import  ProductoForm

class ProductoListView(ListView):
    model = Producto
    template_name = 'producto_list.html'
    context_object_name = 'productos'

class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'producto_detail.html'
    context_object_name = 'producto'

    def get_success_url(self):
        return reverse('productos_listar')

class ProductoCreateView(CreateView):
    model = Producto
    form_class=  ProductoForm
    template_name = 'producto_create.html'
    success_url = reverse_lazy('producto_list')
    

class ProductoUpdateView(UpdateView):
    model = Producto    
    form_class= ProductoForm
    template_name = 'producto_update.html'
    success_url = reverse_lazy('producto_list')

class ProductoDeleteView(DeleteView):
    model = Producto
    template_name = 'producto_delete.html'
    success_url = reverse_lazy('producto_list')