from django.shortcuts import redirect

from .utils import get_or_create_order
from carts.utils import get_or_create_car

def validate_cart_and_order(function):
    def wrap(request, *args, **kwargs):
        cart = get_or_create_car(request)

        if not cart.contains_products():
            return redirect('carts:cart')

        order = get_or_create_order(cart, request)

        return function(request, cart, order)

    return wrap


def validate_order(function):
    def wrap(request, cart, order, *args, **kwargs):
        if not order.billing_profile or not order.user or not order.user.customer_id:
            return redirect('carts:cart')

        return function(request, cart, order)

    return wrap
