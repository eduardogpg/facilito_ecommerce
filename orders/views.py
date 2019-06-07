from django.shortcuts import render
from django.shortcuts import redirect

from carts.utils import get_or_create_car
from .utils import get_or_create_order

def order(request):
    cart_obj = get_or_create_car(request)
    if cart_obj.products.count() == 0:
        return redirect('carts:cart')

    order_obj = get_or_create_order(cart_obj)

    return render(request, 'orders/order.html', {
        'order': order_obj,
        'cart': cart_obj
    })
