from django.urls import reverse

from .models import Order

def breadcrumb(products=True, addres=False, pay=False, confirmation=False):
    return [
        { 'title': 'Productos', 'active': products, 'url': reverse('orders:order') },
        { 'title': 'Dirección', 'active': addres, 'url': reverse('orders:shipping_address') },
        { 'title': 'Pago', 'active': pay, 'url': '/orden' },
        { 'title': 'Confirmación', 'active': confirmation, 'url': '/orden' },
    ]


def get_or_create_order(cart):
    order = Order.objects.filter(cart_id=cart.id).first()
    if not order:
        order = Order.objects.create(cart=cart)

    return order
