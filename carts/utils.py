from .models import Cart
from .common import CartStatus

def get_or_create_car(request):
    cart = None
    user = request.user if request.user.is_authenticated else None

    if user:
        cart = request.user.cart_set.filter(status=CartStatus.CREATED).first()

    if cart is None:
        cart = Cart.objects.filter(cart_id=request.session.get('cart_id')).first()

    if cart is None:
        cart = Cart.objects.create(user=user)

    if user and cart.user is None:
        cart.user = user
        cart.save()

    request.session['cart_id'] = cart.cart_id
    return cart

def destroy_cart(request):
    request.session['cart_id'] = None
