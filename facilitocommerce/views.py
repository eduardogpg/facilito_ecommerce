from django.shortcuts import render
#from django.http import HttpResponse
#return HttpResponse('Hola mundo')
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

    if request.method == 'POST':
        print("Peticón POST: "request.POST.get('username'))
        print("Formulario : "form['username'].data)

    return render(request, 'login.html', context)
