from django.contrib import admin
from django.urls import path

from .views import home, login

urlpatterns = [
    path('', home),
    path('login/', login),
    path('admin/', admin.site.urls),
]
