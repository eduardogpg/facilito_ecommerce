from django.urls import reverse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from .models import BillingProfile
from .forms import BillingProfileForm

class BillingProfileUpdate(SuccessMessageMixin, UpdateView):
    model = BillingProfile
    form_class = BillingProfileForm
    template_name = 'billing_profiles/update.html'
    success_message = 'Dirección actualizada exitosamente.'
    #success_url = reverse_lazy('orders:order')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().id: #Podemos hacer uso del método get_object cuantas veces necesitemos
            return redirect('carts:cart')

        return super(BillingProfileUpdate, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super(BillingProfileUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse('billing_profiles:edit', kwargs={
            'pk': self.object.pk
        })

class BillingProfileDelete(SuccessMessageMixin, DeleteView):
    model = BillingProfile
    template_name = 'billing_profiles/delete.html'
    success_url = reverse_lazy('home')
    success_message = 'Dirección eliminada exitosamente.'
