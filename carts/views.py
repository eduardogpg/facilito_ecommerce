from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from .utils import get_or_create_car

from products.models import Product

def cart(request):
    return render(request, 'carts/cart.html', {
        'cart': get_or_create_car(request)
    })

def add(request):
    product_obj = get_object_or_404(Product, id=request.POST.get('product_id', 7))
    cart_obj = get_or_create_car(request)
    cart_obj.products.add(product_obj)

    return render(request, 'carts/add.html', {
        'cart': cart_obj, 'product': product_obj,
        'message_product': 'productos' if cart_obj.products.count() > 1 else 'producto'
    })

def remove(request):
    cart_obj = get_or_create_car(request)
    product_obj = get_object_or_404(Product, id=request.POST.get('product_id'))
    if product_obj in cart_obj.products.all():
        cart_obj.products.remove(product_obj)

    return redirect('carts:cart')
