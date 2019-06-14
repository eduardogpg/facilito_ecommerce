from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.generic.list import ListView

from shipping_addresses.models import ShippingAddress
from shipping_addresses.forms import ShippingAddressForm

from .models import Order
from .models import StatusChoice

from .utils import breadcrumb
from .utils import get_or_create_order

from carts.utils import destroy_cart
from carts.utils import get_or_create_car

class OrdersListView(ListView):
    model = Order
    template_name = 'orders/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = context['order_list'].count()
        context['message_order'] = 'Pedidos' if context['count'] > 1 else 'Pedido'

        return context

    def get_queryset(self):
        return Order.objects.filter(status=StatusChoice.COMPLETED).filter(user_id=1).order_by('-id')

@login_required(login_url='login')
def order(request):
    cart = get_or_create_car(request)

    if not cart.contains_products():
        return redirect('carts:cart')

    order = get_or_create_order(cart, request)

    return render(request, 'orders/order.html', {
        'cart': cart,
        'order': order,
        'breadcrumb': breadcrumb()
    })

@login_required(login_url='login')
def address(request):
    cart = get_or_create_car(request)

    if not cart.contains_products():
        return redirect('carts:cart')

    order = get_or_create_order(cart, request)

    shipping_address = order.get_or_set_default_shipping_address()
    choose_other_address = request.user.shippingaddress_set.filter(default=False).exists()

    return render(request, 'orders/address.html', {
        'cart':cart, 'order': order,
        'shipping_address': shipping_address,
        'choose_other_address': choose_other_address,
        'breadcrumb': breadcrumb(addres=True)
    })

@login_required(login_url='login')
def select_address(request):
    shipping_addresses = request.user.shippingaddress_set.filter(default=False)

    return render(request, 'orders/select_address.html', {
        'shipping_addresses': shipping_addresses,
        'breadcrumb': breadcrumb(addres=True)
    })

@login_required(login_url='login')
def check_address(request, pk):
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    cart = get_or_create_car(request)

    if not cart.contains_products():
        return redirect('carts:cart')

    order = get_or_create_order(cart, request)

    order.shipping_address = shipping_address
    order.save()

    return redirect('orders:address')

@login_required(login_url='login')
def confirm(request):
    cart = get_or_create_car(request)

    if not cart.contains_products():
        return redirect('carts:cart')

    order = get_or_create_order(cart, request)

    if not order.shipping_address:
        return redirect('orders:address')

    shipping_address = order.shipping_address
    return render(request, 'orders/confirm.html', {
        'order': order, 'cart': cart,
        'shipping_address': shipping_address,
        'breadcrumb': breadcrumb(addres=True, pay=True, confirmation=True)
    })

@login_required(login_url='login')
def complete(request):
    cart = get_or_create_car(request)

    if not cart.contains_products():
        return redirect('carts:cart')

    order = get_or_create_order(cart, request)

    if not order.shipping_address:
        return redirect('orders:address')

    cart.complete()
    order.complete()

    destroy_cart(request)

    messages.success(request, 'Compra completada exitosamente.')
    return redirect('carts:cart')
