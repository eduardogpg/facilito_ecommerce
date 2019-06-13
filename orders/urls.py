from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order, name='order'),
    path('direccion', views.shipping_address, name='shipping_address'),
    path('direccion/seleccionar', views.select_shipping_address, name='select_shipping_address'),
    path('direccion/check/<int:pk>', views.check_shipping_address, name='check_shipping_address'),
]
