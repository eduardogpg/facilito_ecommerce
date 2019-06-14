from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order, name='order'),
    path('confirmar', views.confirm, name='confirm'),
    path('completar', views.complete, name='complete'),
    path('direccion', views.address, name='address'),
    path('direccion/seleccionar', views.select_address, name='select_address'),
    path('direccion/check/<int:pk>', views.check_address, name='check_address'),
]
