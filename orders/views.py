from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from billing_profiles.models import BillingProfile
from billing_profiles.forms import BillingProfileForm

from carts.utils import get_or_create_car
from .utils import get_or_create_order

def order(request):
    cart = get_or_create_car(request)
    if cart.products.count() == 0 :
        return redirect('carts:cart')

    order = get_or_create_order(cart)

    return render(request, 'orders/order.html', {
        'order': order, 'cart': cart
    })

def complete(request):
    form = BillingProfileForm(request.POST or None)
    cart = get_or_create_car(request)
    order = get_or_create_order(cart)

    if request.method == 'POST' and form.is_valid():
        billing_profile = form.save(commit=False)
        billing_profile.user = request.user
        billing_profile.save()

        order.billing_profile = billing_profile
        order.save()

    return render(request, 'orders/complete.html', {
        'billing_profile': request.user.billingprofile_set.first(),
        'form': form,
    })
