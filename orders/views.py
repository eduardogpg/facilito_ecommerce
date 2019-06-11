from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
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

    billing_profile = order.billing_profile
    if not billing_profile:
        billing_profile = request.user.billingprofile_set.filter(default=True).first()

    return render(request, 'orders/billing_address.html', {
        'billing_profile': billing_profile,
        'form': form,
        'breadcrumb': breadcrumb(addres=True)
    })

@login_required(login_url='login')
def select_billing_address(request):
    billing_profiles = request.user.billingprofile_set.filter(default=False)

    return render(request, 'orders/select_billing_address.html', {
        'billing_profiles': billing_profiles,
        'breadcrumb': breadcrumb(addres=True)
    })

@login_required(login_url='login')
def check_billing_address(request, pk):
    billing_profile = get_object_or_404(BillingProfile, pk=pk)

    if request.user.id != billing_profile.user_id:
        return redirect('home')

    cart = get_or_create_car(request)
    order = get_or_create_order(cart)

    order.billing_profile = billing_profile
    order.save()

    return redirect('orders:billing_address')
