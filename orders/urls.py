from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order, name='order'),
    path('pago', views.payment, name='payment'),
    path('cancelar', views.cancel, name='cancel'),
    path('confirmar', views.confirm, name='confirm'),
    path('completar', views.complete, name='complete'),
    path('direccion/envio', views.address, name='address'),
    path('seleccionar/direccion/envio', views.select_address, name='select_address'),
    path('establecer/direccion/envio/<int:pk>', views.check_address, name='check_address'),
]
