from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from .utils import get_or_create_car

from .models import CartProducts
from products.models import Product

def cart(request):
    cart = get_or_create_car(request)
    count = cart.products.count()

    return render(request, 'carts/cart.html', {
        'cart': cart,
        'count': count,
    })

def add(request):
    product = get_object_or_404(Product, id=request.POST.get('product_id') )

    cart = get_or_create_car(request)
    # cart.products.add(product, through_defaults={
    #     'quantity': request.POST.get('quantity', 1)
    # })

    cart_product = CartProducts.objects.create(product=product,
                                cart=cart,
                                quantity=request.POST.get('quantity', 1))

    return render(request, 'carts/add.html', {
        'cart': cart,
        'product': product,
        'cart_product': cart_product,
    })

def remove(request):
    cart = get_or_create_car(request)
    product = get_object_or_404(Product, id=request.POST.get('product_id'))

    cart.products.remove(product)

    return redirect('carts:cart')
