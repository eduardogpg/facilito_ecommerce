from django.contrib import admin

from .models import Cart
from .models import CartProducts

admin.site.register(Cart)
admin.site.register(CartProducts)
