from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from billing_profiles.models import BillingProfile
from billing_profiles.forms import BillingProfileForm

from .utils import breadcrumb
from .utils import get_or_create_order
from carts.utils import get_or_create_car

@login_required(login_url='login')
def order(request):
    cart = get_or_create_car(request)
    if cart.products.count() == 0 :
        messages.warning(request, 'Tu carrito esta vacío.')
        return redirect('carts:cart')

    order = get_or_create_order(cart)

    return render(request, 'orders/order.html', {
        'cart': cart,
        'order': order,
        'breadcrumb': breadcrumb()
    })

@login_required(login_url='login')
def billing_address(request):
    cart = get_or_create_car(request)
    order = get_or_create_order(cart)
    form = BillingProfileForm(request.POST or None)
    billing_profile = request.user.billingprofile_set.first()

    if request.method == 'POST' and form.is_valid():
        billing_profile = form.save(commit=False)
        billing_profile.user = request.user
        billing_profile.save()

        order.billing_profile = billing_profile
        order.save()

    return render(request, 'orders/billing_address.html', {
        'billing_profile': billing_profile,
        'form': form,
        'breadcrumb': breadcrumb(addres=True)
    })
