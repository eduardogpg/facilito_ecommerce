from django.contrib import admin
from django.urls import path, include

from .views import home, register, logout_view, login_user as login

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('usuario/login', login, name='login'),
    path('usuario/logout', logout_view, name='logout'),
    path('usuario/registro', register, name='register'),
]
