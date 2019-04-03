from django.shortcuts import render

#https://docs.djangoproject.com/en/2.2/topics/auth/default/#authenticating-users
from django.contrib.auth import authenticate, login as django_login

from .forms import LoginForm

def home(request):
    context = {
        'title': 'Listado de productos',
        'message': 'Productos',
        'products': [
            {'title': 'Playeras', 'stock': True},
            {'title': 'Tazas', 'stock': True},
            {'title': 'Art toy', 'stock': True},
            {'title': 'Peluches', 'stock': False},
        ]
    }
    return render(request, 'home_page.html', context)

def login(request):
    form = LoginForm(request.POST or None)
    context = {
        'title': 'Login',
        'form': form
    }

    if request.method == 'POST' and form.is_valid():
        print("Username : ", form['username'].data)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            django_login(request, user)
            print("Usuario autenticado exitosamente!")

    return render(request, 'login.html', context)
