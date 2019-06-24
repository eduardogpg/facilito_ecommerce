import uuid
import decimal

from django.db import models

from profiles.models import User #from django.contrib.auth.models import User
from django.db.models.signals import pre_save, m2m_changed

from .common import choices
from .common import CartStatus
from orders.common import OrderStatus

from products.models import Product

class Cart(models.Model):
    cart_id = models.CharField(max_length=100, null=False, blank=True, unique=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE) #One to Many, a user could have many carts
    products = models.ManyToManyField(Product, blank=True, through='CartProducts')
    subtotal = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=choices, default=CartStatus.CREATED)

    FEE = 0.05

    def __str__(self):
        return self.cart_id

    def contains_products(self):
        return self.products.exists()

    def update_subtotal(self):
        #self.subtotal = sum( [product.price for product in self.products.all()] )
        self.subtotal = sum( [cp.product.price * cp.quantity for cp in self.products_related()] )
        self.save()

    def update_total(self):
        self.total = self.subtotal + (self.subtotal * decimal.Decimal(Cart.FEE))
        self.save()

    def complete(self):
        self.status = CartStatus.CLOSED
        self.save()

    def close(self):
        self.status = CartStatus.CLOSED
        self.save()

    def total_products(self):
        return sum( [cp.quantity for cp in self.cartproducts_set.all()] )

    def products_related(self):
        return self.cartproducts_set.select_related('product')

    @property
    def order(self):
        return self.order_set.filter(status=OrderStatus.CREATED).first()

class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now=True)

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
        pass

pre_save.connect(generate_cart_id, sender=Cart)
#
# m2m_changed.connect(calculate_subtotal, sender=Cart.products.through)
# m2m_changed.connect(calculate_total, sender=Cart.products.through)
# m2m_changed.connect(calculate_order_total, sender=Cart.products.through)
