import uuid
import decimal
import datetime

from .common import choices
from .common import OrderStatus

from django.db import models
from django.dispatch import receiver

from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed

from carts.models import Cart
from profiles.models import User
from promo_codes.models import PromoCode
#from django.contrib.auth.models import User

from billing_profiles.models import BillingProfile
from shipping_addresses.models import ShippingAddress

class Order(models.Model):
    #related_name
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, null=False, blank=True, unique=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=choices, default=OrderStatus.CREATED)
    shipping_total = models.DecimalField(default=4.69, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    shipping_address = models.ForeignKey(ShippingAddress, #Una dirección de envío puede tener muchas ordenes
                                            null=True, blank=True,
                                            on_delete=models.CASCADE)

    promo_code = models.OneToOneField(PromoCode, #Una promoción puede tener una orden
                                        null=True, blank=True,
                                        default=None,
                                        on_delete=models.CASCADE)

    billing_profile = models.ForeignKey(BillingProfile, #Un método de pago puede tener muchas ordenes
                                            null=True, blank=True,
                                            on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.order_id

    def get_or_set_default_shipping_address(self):
        if self.shipping_address_id:
            return self.shipping_address

        shipping_address = self.user.default_address

        if shipping_address:
            self.shipping_address = shipping_address
            self.save()

        return shipping_address

    def get_or_set_default_billing_profile(self):
        if self.billing_profile_id:
            return self.billing_profile

        billing_profile = self.user.default_billing_profile

        if billing_profile:
            self.billing_profile = billing_profile
            self.save()

        return billing_profile

    def update_total(self):
        self.total = self.calculate_total()
        self.save()

    def get_discount(self):
        if not self.promo_code_id:
            return 0

        return decimal.Decimal(self.promo_code.discount)

    def calculate_total(self):
        return self.cart.total + decimal.Decimal(self.shipping_total) - self.get_discount()

    def complete(self):
        self.status = OrderStatus.COMPLETED
        self.save()

    def cancel(self):
        self.status = OrderStatus.CANCELED
        self.save()

    def apply_promo_code(self, promo_code):
        self.promo_code = promo_code
        self.save()
        self.update_total()
        promo_code.use()

def generate_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = str(uuid.uuid4())

def calculate_total(sender, instance, *args, **kwargs):
    instance.total = instance.calculate_total()

pre_save.connect(generate_order_id, sender=Order)
pre_save.connect(calculate_total, sender=Order)
