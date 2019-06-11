from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from .utils import get_or_create_car

from products.models import Product

def cart(request):
    cart = get_or_create_car(request)
    count = cart.products.count()

    return render(request, 'carts/cart.html', {
        'cart': cart,
        'count': count,
        'message_product': 'productos' if count > 1 else 'producto'
    })

def add(request):
    product = get_object_or_404(Product, id=request.POST.get('product_id') )
    cart = get_or_create_car(request)
    cart.products.add(product)
    
    return render(request, 'carts/add.html', {
        'cart': cart, 'product': product,
        'message_product': 'productos' if cart.products.count() > 1 else 'producto'
    })

def remove(request):
    cart = get_or_create_car(request)
    product = get_object_or_404(Product, id=request.POST.get('product_id'))
    if product in cart.products.all():
        cart.products.remove(product)

    return redirect('carts:cart')
