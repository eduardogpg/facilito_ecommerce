import uuid

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, m2m_changed

from carts.models import Cart

class Order(models.Model):
    STATUS_CHOICES = (
        ('C', 'CREATED'),
    )
    order_id = models.CharField(max_length=100, null=False, blank=True, unique=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='c')
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)

    def __str__(self):
        return self.order_id

def generate_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())

def calculate_total(sender, instance, *args, **kwargs):
    instance.total = instance.cart.total

def calculate_total_by_cart(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        Order.objects.filter(cart_id=instance.id).update(total=instance.total)

pre_save.connect(generate_order_id, sender=Order)
pre_save.connect(calculate_total, sender=Order)

m2m_changed.connect(calculate_total_by_cart, sender=Cart.products.through)
