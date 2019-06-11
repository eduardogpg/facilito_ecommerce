from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order, name='order'),
    path('direccion', views.billing_address, name='billing_address'),
    path('direccion/seleccionar', views.select_billing_address, name='select_billing_address'),
    path('direccion/check/<int:pk>', views.check_billing_address, name='check_billing_address'),
]
