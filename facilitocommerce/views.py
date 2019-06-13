from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from .forms import RegisterForm

def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        if user:
            login(request, user)
            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('home')

    return render(request, 'user/register.html', { 'form': form })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Te damos la bienvenida {}'.format(user.username))

            if request.GET.get('next'):
                return HttpResponseRedirect(request.GET['next'])

            return redirect('home')

    return render(request, 'user/login.html', {})

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente')
    return redirect('login')
