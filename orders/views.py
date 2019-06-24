from .mail import Mail

from django.db import transaction

from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import reverse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from django.views.generic.list import ListView

from django.db.models.query import EmptyQuerySet

from shipping_addresses.models import ShippingAddress
from shipping_addresses.forms import ShippingAddressForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Order
from .common import OrderStatus

from .utils import get_order
from .utils import breadcrumb
from .utils import destroy_order

from .decorators import validate_order
from .decorators import validate_cart_and_order

from carts.utils import destroy_cart
from carts.utils import get_or_create_car

from charges.models import Charge
from profiles.models import Customer

from stripeAPI.charge import create_charge

class OrdersListView(LoginRequiredMixin, ListView):
    model = Order
    login_url = 'login'
    template_name = 'orders/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer = Customer.get_customer(self.request.user)
        if customer:
            context['customer'] = customer
            context['orders_completed'] = customer.orders_completed()

        return context

    def get_queryset(self):
        return EmptyQuerySet

@login_required(login_url='login')
@validate_cart_and_order
def order(request, cart, order):
    return render(request, 'orders/order.html', {
        'cart': cart,
        'order': order,
        'breadcrumb': breadcrumb()
    })

@login_required(login_url='login')
@validate_cart_and_order
def address(request, cart, order):
    shipping_address = order.get_or_set_default_shipping_address()
    choose_other_address = request.user.shippingaddress_set.filter(default=False).exists()

    return render(request, 'orders/address.html', {
        'cart':cart, 'order': order,
        'shipping_address': shipping_address,
        'choose_other_address': choose_other_address,
        'title':'Dirección de envío',
        'next_url': reverse('orders:address'),
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
@validate_cart_and_order
def check_address(request, cart, order, pk):
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    order.shipping_address = shipping_address
    order.save()

    return redirect('orders:address')

@login_required(login_url='login')
@validate_cart_and_order
def payment(request, cart, order):
    billing_profile = order.get_or_set_default_billing_profile()

    return render(request, 'orders/payment.html', {
        'cart': cart, 'order': order,
        'billing_profile': billing_profile,
        'title': 'Método de pago',
        'next_url': reverse('orders:payment'),
        'breadcrumb': breadcrumb(addres=True, payment=True)
    })

@login_required(login_url='login')
@validate_cart_and_order
def confirm(request, cart, order):
    if not order.shipping_address:
        return redirect('orders:address')

    shipping_address = order.shipping_address
    return render(request, 'orders/confirm.html', {
        'order': order, 'cart': cart,
        'shipping_address': shipping_address,
        'breadcrumb': breadcrumb(addres=True, payment=True, confirmation=True)
    })

@login_required(login_url='login')
@validate_cart_and_order
@validate_order
def complete(request, cart, order):
    charge = Charge.create_charge_by_order(order)
    if charge:
        with transaction.atomic():
            cart.complete()
            order.complete()
            Mail.send_complete_order_mail(order, request.user)

            destroy_cart(request)
            destroy_order(request)

    messages.success(request, 'Compra completada exitosamente.')
    return redirect('carts:cart')

@login_required(login_url='login')
@validate_cart_and_order
def cancel(request, cart, order):
    order.cancel()
    cart.close()

    destroy_cart(request)
    destroy_order(request)

    messages.error(request, 'Orden cancelada')
    return redirect('carts:cart')
