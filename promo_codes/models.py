import string
import random

from django.db import models
from django.utils import timezone

from django.db.models.signals import pre_save

class PromoCodeManager(models.Manager):

    def get_valid(self, code):
        now = timezone.now()
        return self.filter(code=code).filter(active=True).first()#.filter(valid_from__gte=now).filter(valid_to__lt=now).first()

class PromoCode(models.Model):
    code = models.CharField(max_length=50)
    discount = models.FloatField(default=0.0)
    valid_to = models.DateTimeField()
    valid_from = models.DateTimeField()
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PromoCodeManager()

    LEN = 8

    def __str__(self):
        return self.code

    def use(self):
        #self.active = False
        self.save()

    @property
    def used(self):
        return not self.active

def generate_code(sender, instance, *args, **kwargs):
    if instance.code:
        return

    chars = string.ascii_uppercase + string.digits
    instance.code = ''.join(random.choice(chars) for _ in range(PromoCode.LEN))

pre_save.connect(generate_code, sender=PromoCode)
