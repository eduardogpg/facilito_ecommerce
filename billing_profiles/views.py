from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import BillingProfile
from .forms import BillingProfileForm

@login_required(login_url='login')
def create(request):
    form = BillingProfileForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        billing_profile = form.save(commit=False)
        billing_profile.user = request.user
        billing_profile.default = not request.user.billingprofile_set.filter(default=True).exists()
        billing_profile.save()

        messages.success(request, 'Dirección creada exitosamente.')
        return redirect('billing_profiles:billing_profiles')

    return render(request, 'billing_profiles/create.html', {
        'form': form
    })

@login_required(login_url='login')
def default(request, pk):
    billing_profile = get_object_or_404(BillingProfile, pk=pk)

    if request.user.id != billing_profile.user_id:
        return redirect('home')

    request.user.billingprofile_set.filter(default=True).update(default=False)

    billing_profile.set_default()

    messages.success(request, 'Dirección principal actualizada')

    return redirect('billing_profiles:billing_profiles')

class BillingProfileListView(LoginRequiredMixin, ListView):
    login_url = 'home'
    model = BillingProfile
    template_name = 'billing_profiles/billing_profiles.html'

    def get_queryset(self):
        return BillingProfile.objects.filter(user=self.request.user).order_by('-default')

class BillingProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'home'
    model = BillingProfile
    form_class = BillingProfileForm
    template_name = 'billing_profiles/update.html'
    success_message = 'Dirección actualizada exitosamente.'

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().user_id:
            return redirect('carts:cart')

        return super(BillingProfileUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('billing_profiles:billing_profiles', kwargs={
            #'pk': self.object.pk
        })

class BillingProfileDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'home'
    model = BillingProfile
    template_name = 'billing_profiles/delete.html'
    success_message = 'Dirección eliminada exitosamente.'
    success_url = reverse_lazy('billing_profiles:billing_profiles')

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().default:
            return redirect('billing_profiles:billing_profiles')

        return super(BillingProfileDeleteView, self).dispatch(request, *args, **kwargs)
