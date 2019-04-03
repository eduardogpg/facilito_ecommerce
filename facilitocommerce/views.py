from django.shortcuts import render
#from django.http import HttpResponse

def home_page(request):
    #return HttpResponse('Hola mundo')
    return render(request, 'home_page.html', {})
