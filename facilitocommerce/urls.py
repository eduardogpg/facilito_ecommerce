from django.contrib import admin
from django.urls import path

from .views import home, register

urlpatterns = [
    path('', home),
    path('registro/', register),
    path('admin/', admin.site.urls),
]
