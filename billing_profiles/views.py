from django.shortcuts import render

from .forms import BillingProfileForm

def edit(request):
    return redirect(request, 'billing_profiles/edit.html', {
        'form': form
    })
