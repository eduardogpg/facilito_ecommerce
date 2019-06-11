from django.urls import path

from . import views

app_name = 'billing_profiles'

urlpatterns = [
    path('editar/<int:pk>', views.BillingProfileUpdate.as_view(), name='edit'),
    path('eliminar/<int:pk>', views.BillingProfileDelete.as_view(), name='delete'),
]
