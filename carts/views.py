from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .utils import get_or_create_car

from products.models import Product

def cart(request):
    return render(request, 'carts/cart.html', {
        'cart_obj': get_or_create_car(request)
    })

def add(request):
    product_obj = get_object_or_404(Product, id=request.POST.get('product_id'))
    cart_obj = get_or_create_car(request)
    cart_obj.products.add(product_obj)

    return render(request, 'carts/add.html', {
        'cart': cart_obj, 'product': product_obj
    })

def remove(request):
    product_obj = Product.objects.get(id=1)
    cart_obj = get_or_create_car(request)

    if product_obj in cart_obj.products:
        cart_obj.products.remove(product_obj)
