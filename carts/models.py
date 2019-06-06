from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, m2m_changed

from products.models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

def calculate_subtotal(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.subtotal = sum( [product.price for product in instance.products.all() ])
        instance.save()

def calculate_total(sender, instance, action, *args, **kwargs):
    instance.total = instance.subtotal + 10
    instance.save()

m2m_changed.connect(calculate_subtotal, sender=Cart.products.through)
m2m_changed.connect(calculate_total, sender=Cart.products.through)
