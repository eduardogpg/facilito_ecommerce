from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    #path('<pk>', views.ProductDetailView.as_view()),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='detail'),
]
