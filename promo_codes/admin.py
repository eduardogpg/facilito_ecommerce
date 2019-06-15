from django.contrib import admin

from .models import PromoCode

class PromoCodeAdmin(admin.ModelAdmin):
    #fields = ('discount', 'valid_to', 'valid_from', 'active')
    exclude = ['code']

admin.site.register(PromoCode, PromoCodeAdmin)
