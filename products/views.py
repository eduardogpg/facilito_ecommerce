from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Product

class ProductListView(ListView):

    model = Product
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CodigoFacilito'
        context['promotion_title'] = 'Últimos productos'
        return context

class ProductDetailView(DetailView):

    model = Product
    template_name = 'products/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Producto'
        return context

class ProductSearchListView(ListView):
    template_name = 'products/search.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['count'] = data['product_list'].count()
        return data

    def get_queryset(self):
        query  = self.request.GET.get('q')
        if self.exist_q():
            return Product.objects.filter(title__icontains=query)

        return Product.objects.none()

    def exist_q(self):
        return self.request.GET.get('q') is not None
