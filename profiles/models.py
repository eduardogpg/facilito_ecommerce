from django.db import models
from django.contrib.auth.models import AbstractUser

#https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#extending-the-existing-user-model

class User(AbstractUser):
    pass

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def default_address(self):
        return self.shippingaddress_set.filter(default=True).first()

    @property
    def has_default_address(self):
        self.default_address.exists()


class Profile(User):
    class Meta:
        proxy = True

    def default_address(self):
        return self.shippingaddress_set.filter(default=True).first()
