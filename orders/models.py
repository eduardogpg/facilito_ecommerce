import uuid
import decimal

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, m2m_changed

from carts.models import Cart
from shipping_addresses.models import ShippingAddress

class Order(models.Model):
    STATUS_CHOICES = (
        ('C', 'CREATED'),
    )
    order_id = models.CharField(max_length=100, null=False, blank=True, unique=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='c')
    shipping_total = models.DecimalField(default=4.69, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    shipping_address = models.ForeignKey(ShippingAddress,
                                        null=True, blank=True,
                                        on_delete=models.CASCADE)

    def __str__(self):
        return self.order_id

    def get_or_set_default_shipping_address(self):
        if self.shipping_address_id:
            return self.shipping_address

        shipping_address = self.cart.user.shippingaddress_set.filter(default=True).first()
        if shipping_address:
            self.shipping_address = shipping_address

        return shipping_address

    def update_total(self):
        self.total = self.calculate_total()
        self.save()

    def calculate_total(self):
        return self.cart.total + decimal.Decimal(self.shipping_total)

def generate_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())

def calculate_total(sender, instance, *args, **kwargs):
    instance.total = instance.calculate_total()

pre_save.connect(generate_order_id, sender=Order)
pre_save.connect(calculate_total, sender=Order)
