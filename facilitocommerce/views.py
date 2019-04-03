from django.http import HttpResponse

def home_page(request):
    return HttpResponse('Hola mundo')
