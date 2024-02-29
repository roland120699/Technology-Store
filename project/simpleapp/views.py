from datetime import datetime

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from .filters import ProductFilter
from .forms import ProductForm
from .models import Product

def multiply(request):
   number = request.GET.get('number')
   multiplier = request.GET.get('multiplier')

   try:
       result = int(number) * int(multiplier)
       html = f"<html><body>{number}*{multiplier}={result}</body></html>"
   except (ValueError, TypeError):
       html = f"<html><body>Invalid input.</body></html>"

   return HttpResponse(html)

class ProductsList(ListView):
    model = Product
    ordering = 'name'
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['time_now'] = datetime.utcnow()
        contex['next_sale'] = 'Распродажа в среду!'
        contex['filterset'] = self.filterset
        return contex


class ProductDetail(DetailView):
    model = Product
    template_name = 'product.html'
    contex_object_name = 'product'

class ProductCreate(CreateView):
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'

class ProductUpdate(UpdateView):
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'

class ProductDelete(DeleteView):
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')



















