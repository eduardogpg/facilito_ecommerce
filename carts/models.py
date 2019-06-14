import uuid
import decimal
from enum import Enum

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, m2m_changed

from products.models import Product

class StatusChoice(Enum):
    CREATED = 'CREATED'
    CLOSED = 'CLOSED'

choices = [(tag, tag.value) for tag in StatusChoice]

class Cart(models.Model):
    cart_id = models.CharField(max_length=100, null=False, blank=True, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE) #One to Many, a user could have many carts
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=choices, default=StatusChoice.CREATED)

    FEE = 0.05

    def __str__(self):
        return self.cart_id

    def update_subtotal(self):
        self.subtotal = self.calculate_subtotal()
        self.save()

    def update_total(self):
        self.total = self.calculate_total()
        self.save()

    def calculate_subtotal(self):
        return sum( [product.price for product in self.products.all()] )

    def calculate_total(self):
        return self.subtotal + (self.subtotal * decimal.Decimal(Cart.FEE))

    def contains_products(self):
        return self.products.exists()

    def complete(self):
        self.status = StatusChoice.CLOSED
        self.save()

    def close(self):
        self.status = StatusChoice.CLOSED
        self.save()

def generate_cart_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())

def calculate_subtotal(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.update_subtotal()

def calculate_total(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.update_total()

def calculate_order_total(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        order = instance.order_set.first()
        if order:
            order.update_total()

pre_save.connect(generate_cart_id, sender=Cart)

m2m_changed.connect(calculate_subtotal, sender=Cart.products.through)
m2m_changed.connect(calculate_total, sender=Cart.products.through)
m2m_changed.connect(calculate_order_total, sender=Cart.products.through)
