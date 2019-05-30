from django.shortcuts import render

from .models import Cart

def get_cart(request):
    user = request.user if request.user.is_authenticated else None
    
    cart = Cart.objects.filter(id=request.session.get('card_id')).first()
    if not cart:
        cart = Cart.objects.create(user=user)

    request.session['card_id'] = cart.id
    return cart

def cart(request):
    cart = get_cart(request)
    return render(request, 'carts/cart.html', {})
