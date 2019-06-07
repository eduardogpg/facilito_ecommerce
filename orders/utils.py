from .models import Order

def get_or_create_order(cart):
    order = Order.objects.filter(cart_id=cart.id).first()
    if not order:
        order = Order.objects.create(cart=cart)

    return order
