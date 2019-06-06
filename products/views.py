from django.db.models import Q
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Product

class ProductListView(ListView):

    model = Product
    template_name = 'home.html'
    queryset = Product.objects.last()

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
        data['query'] = self.query() if self.exists_query() else ''
        return data

    def get_queryset(self):
        print("\nEduardo Ismael")
        if self.exists_query():
            query = Q(title__icontains=self.query()) | Q(tag__title__icontains=self.query())
            return Product.objects.filter(query).distinct()

        return Product.objects.none()

    def query(self):
        return self.request.GET.get('q')

    def exists_query(self):
        return self.query() is not None
