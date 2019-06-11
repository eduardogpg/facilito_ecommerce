from django.urls import path

from . import views

app_name = 'billing_profiles'

urlpatterns = [
    path('', views.BillingProfileListView.as_view(), name='billing_profiles'),
    path('nuevo', views.create, name='create'),
    path('editar/<int:pk>', views.BillingProfileUpdateView.as_view(), name='edit'),
    path('eliminar/<int:pk>', views.BillingProfileDeleteView.as_view(), name='delete'),
    path('default/<int:pk>', views.default, name='default')
]
