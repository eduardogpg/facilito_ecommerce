from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User

class BillingProfile(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    streat = models.CharField(max_length=200)
    state = models.CharField(max_length=50)
    phone = models.IntegerField()
    reference = models.CharField(max_length=300)
    zip = models.CharField(max_length=10, null=False, blank=False)
    default = models.BooleanField(default=False)
    
    def __str__(self):
        return self.zip
