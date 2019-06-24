from django.conf import settings
from django.contrib import messages

from .models import BillingProfile
from django.shortcuts import render
from django.shortcuts import redirect

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
def create(request):
    if request.method == 'POST':
        if request.POST.get('stripeToken'):

            if not request.user.has_billing_profile():
                request.user.create_customer_id()

            billing_profile = BillingProfile.create_by_stripe_token(request.user, request.POST['stripeToken'])
            
            if billing_profile:
                messages.success(request, 'Método de pago registrado exitosamente.')

                if request.GET.get('next'):
                    order = get_order(request)
                    order.billing_profile = billing_profile
                    order.save()

                    return HttpResponseRedirect(request.GET['next'])

        else:
            messages.error(request, 'No es pobile completar la operación contacta con un administrador')

    return render(request, 'billing_profiles/new.html', {
        'stripe_key': settings.STRIPE_PUBLIC_KEY,
    })
