import uuid
import decimal

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, m2m_changed

from products.models import Product

class Cart(models.Model):
    cart_id = models.CharField(max_length=100, null=False, blank=True, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    FEE = 0.05

    def __str__(self):
        return self.cart_id

def generate_cart_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())

def calculate_subtotal(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.subtotal = sum( [product.price for product in instance.products.all() ])
        instance.save()

def calculate_total(sender, instance, action, *args, **kwargs):
    if instance.subtotal:
        instance.total = instance.subtotal + (instance.subtotal * decimal.Decimal(Cart.FEE))
        instance.save()

pre_save.connect(generate_cart_id, sender=Cart)

m2m_changed.connect(calculate_subtotal, sender=Cart.products.through)
m2m_changed.connect(calculate_total, sender=Cart.products.through)
