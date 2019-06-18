from django.urls import reverse

from .models import Order

def breadcrumb(products=True, addres=False, payment=False, confirmation=False):
    return [
        { 'title': 'Productos', 'active': products, 'url': reverse('orders:order') },
        { 'title': 'Dirección', 'active': addres, 'url': reverse('orders:address') },
        { 'title': 'Pago', 'active': payment, 'url':reverse('orders:payment') },
        { 'title': 'Confirmación', 'active': confirmation, 'url': reverse('orders:confirm') },
    ]

def get_or_create_order(cart, request):
    order = Order.objects.filter(cart_id=cart.id).first()

    if not order and request.user.is_authenticated:
        order = Order.objects.create(cart=cart, user=request.user)

    request.session['order_id'] = order.order_id
    return order

def get_order(request):
    return Order.objects.filter(order_id=request.session.get('order_id')).first()

def destroy_order(request):
    request.session['order_id'] = None
