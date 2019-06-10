from django.contrib import admin
from django.urls import path, include

from . import views
from products.views import ProductListView

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('usuario/login', views.login_view, name='login'),
    path('usuario/logout', views.logout_view, name='logout'),
    path('usuario/registro', views.register_view, name='register'),
    path('productos/', include('products.urls')),
    path('carrito/', include('carts.urls')),
    path('orden/', include('orders.urls')),
    path('direccion/', include('billing_profiles.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
