from django.db import models
from django.contrib.auth.models import AbstractUser

#https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#extending-the-existing-user-model
class User(AbstractUser):
    customer_id = models.CharField(max_length=100, blank=True, null=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def default_address(self):
        return self.shippingaddress_set.filter(default=True).first()

    @property
    def has_default_address(self):
        return self.shippingaddress_set.filter(default=True).exists()

    @property
    def has_billing_profile(self):
        return self.billingprofile_set.exists()

    @property
    def default_billing_profile(self):
        return self.billingprofile_set.filter(default=True).exists()
    
