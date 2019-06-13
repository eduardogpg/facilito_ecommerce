from django.db import models
from django.contrib.auth.models import User

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    reference = models.CharField(max_length=300)
    zip = models.CharField(max_length=10, null=False, blank=False)
    default = models.BooleanField(default=False)

    def set_default(self):
        self.default = True
        self.save()
    
    @property
    def city_format(self):
        return '{} - {} - {}'.format(self.city, self.state, self.country)

    def __str__(self):
        return self.zip
