from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from billing_profiles.models import BillingProfile
from billing_profiles.forms import BillingProfileForm

from carts.utils import get_or_create_car
from .utils import get_or_create_order

@login_required
def order(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Es necesario iniciar sessión')
        return redirect('carts:cart')

    cart_obj = get_or_create_car(request)
    if cart_obj.products.count() == 0 :
        return redirect('carts:cart')

    order_obj = get_or_create_order(cart_obj)

    return render(request, 'orders/order.html', {
        'order': order_obj,
        'cart': cart_obj
    })

@login_required(login_url='login')
def complete(request):
    form = BillingProfileForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        billing_profile = form.save(commit=False)
        billing_profile.user = request.user
        billing_profile.save()

    return render(request, 'orders/complete.html', {
        'billing_profile': request.user.billingprofile_set.first(),
        'form': form,
    })
