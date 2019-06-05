from .models import Cart

def get_or_create_car(request):
    user = request.user if request.user.is_authenticated else None
    
    cart = Cart.objects.filter(id=request.session.get('card_id')).first()
    if not cart:
        cart = Cart.objects.create(user=user)
    elif cart.user is None and user:
        cart.user = user
        cart.save()

    request.session['card_id'] = cart.id
    return cart
