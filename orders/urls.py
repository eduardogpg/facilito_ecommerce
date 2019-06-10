from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order, name='order'),
    path('completar/direccion', views.complete, name='complete'),
    path('completar/pago', views.complete, name='complete'),
    path('completar/confirmacion', views.complete, name='complete'),
]
