from django.contrib import admin
from .models import User

class CustomerUserAdmin(admin.ModelAdmin):
    exclude = ('groups', 'superuser_status', 'user_permissions', )

admin.site.register(User, CustomerUserAdmin)
