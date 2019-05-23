from django.shortcuts import render
from django.contrib.auth.models import User

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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if username and password and email:
            user = User.objects.create_user(
                username=username, password=password, email=email,
            )
            #Crear validaciones
            print('Usuario creado exitosamente.')


    return render(request, 'register.html', {})
