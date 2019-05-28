from django.contrib import admin
from django.urls import path, include

from .views import home, register, logout_view, login_user as login
from products.views import ProductListView, ProductDetailView

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('usuario/login', login, name='login'),
    path('usuario/logout', logout_view, name='logout'),
    path('usuario/registro', register, name='register'),
    #path('productos/<pk>', ProductDetailView.as_view()),
    path('productos/', include('products.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
