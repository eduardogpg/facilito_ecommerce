from django.db import models
#from django.contrib.auth.models import User
from profiles.models import User

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    line1 = models.CharField(max_length=200)
    line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    reference = models.CharField(max_length=300, null=False, blank=False)
    postal_code = models.CharField(max_length=10)
    default = models.BooleanField(default=False)

    @classmethod
    def set_default_false(self, user):
        ShippingAddress.objects.filter(user=user).filter(default=True).update(default=False)

    def set_default(self):
        self.default = True
        self.save()

    @property
    def city_format(self):
        return '{} - {} - {}'.format(self.city, self.state, self.country)

    def __str__(self):
        return self.postal_code
