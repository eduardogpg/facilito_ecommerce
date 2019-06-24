from django.conf import settings
from django.contrib import messages

from .models import BillingProfile
from django.shortcuts import render
from django.shortcuts import redirect

from stripeAPI.customer import create_card
from stripeAPI.customer import create_customer

from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

class BillingProfileListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = BillingProfile
    template_name = 'billing_profiles/billing_profile.html'

    def get_queryset(self):
        return BillingProfile.objects.filter(user=self.request.user).order_by('-default')

@login_required(login_url='login')
def new(request):
    return render(request, 'billing_profiles/new.html', {
        'stripe_key': settings.STRIPE_PUBLIC_KEY,
    })

@login_required(login_url='login')
def create(request):
    if request.method == 'POST' and request.POST.get('stripeToken'):

        if not request.user.has_billing_profile():
            create_customer(request.user)

        if create_card(request.user, request.POST['stripeToken']):
            messages.success(request, 'Método de pago registrado exitosamente.')
        else:
            messages.error(request, 'Por ahora no es pobile completar la operación contacta con los administradores')

    else:
        messages.error(request, 'No es posible registrar el método de pago.')

    return redirect('billing_profiles:new')
