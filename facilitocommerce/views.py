from django.shortcuts import render
from django.contrib.auth.models import User

from .forms import RegisterForm

def home(request):
    products = [
        {'name': 'Playera', 'available': True},
        {'name': 'Taza', 'available': True},
        {'name': 'ArtToy', 'available': False}
    ]

    return render(request, 'home.html', {
        'title': 'Productos', 'products': products
    })

def register(request):
    form = RegisterForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            if user:
                print("Usuario registrado exitosamente")

    return render(request, 'register.html', {
        'form': form
    })
