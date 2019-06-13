from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from shipping_addresses.models import ShippingAddress
from shipping_addresses.forms import ShippingAddressForm

from .utils import breadcrumb
from .utils import get_or_create_order
from carts.utils import get_or_create_car

@login_required(login_url='login')
def order(request):
    cart = get_or_create_car(request)

    if not cart.contains_products():
        return redirect('carts:cart')

    order = get_or_create_order(cart)

    return render(request, 'orders/order.html', {
        'cart': cart,
        'order': order,
        'breadcrumb': breadcrumb()
    })

@login_required(login_url='login')
def shipping_address(request):
    cart = get_or_create_car(request)

    if not cart.contains_products():
        return redirect('carts:cart')

    order = get_or_create_order(cart)

    shipping_address = order.get_or_set_default_shipping_address()
    choose_other_address = request.user.shippingaddress_set.filter(default=False).exists()

    return render(request, 'orders/shipping_address.html', {
        'cart':cart, 'order': order,
        'shipping_address': shipping_address,
        'choose_other_address': choose_other_address,
        'breadcrumb': breadcrumb(addres=True)
    })

@login_required(login_url='login')
def select_shipping_address(request):
    shipping_addresses = request.user.shippingaddress_set.filter(default=False)

    return render(request, 'orders/select_shipping_address.html', {
        'shipping_addresses': shipping_addresses,
        'breadcrumb': breadcrumb(addres=True)
    })

@login_required(login_url='login')
def check_shipping_address(request, pk):
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    cart = get_or_create_car(request)

    if not cart.contains_products():
        return redirect('carts:cart')

    order = get_or_create_order(cart)

    order.shipping_address = shipping_address
    order.save()

    return redirect('orders:shipping_address')
