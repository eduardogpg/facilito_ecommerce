from django.contrib import admin
from django.urls import path

from .views import home_page

urlpatterns = [
    path('', home_page),
    path('admin/', admin.site.urls),
]
