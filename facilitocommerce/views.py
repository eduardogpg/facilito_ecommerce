from django.shortcuts import render
#from django.http import HttpResponse
#return HttpResponse('Hola mundo')

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
    context = {
        'title': 'Login'
    }
    if request.method == 'POST':
        print(request.POST)
        print(request.POST.get('username'))
        
    return render(request, 'login.html', context)
