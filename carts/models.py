import uuid
import decimal

from django.db import models

from profiles.models import User #from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.db.models.signals import m2m_changed

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

    def update_totals(self):
        self.update_subtotal()
        self.update_total()

        if self.order:
            self.order.update_total()

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

class CartProductsManager(models.Manager):

    def create_or_update_quantity(self, product, cart, quantity=1):
        object, created = self.get_or_create(product=product, cart=cart)

        if not created:
            quantity = object.quantity + quantity

        object.update_quantity(quantity)
        return object

class CartProducts(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now=True)

    objects = CartProductsManager()

    def update_quantity(self, quantity=1):
        self.quantity = quantity
        self.save()

def generate_cart_id(sender, instance, *args, **kwargs):
    if not instance.cart_id:
        instance.cart_id = str(uuid.uuid4())

def m2m_update_totals(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        instance.update_totals()

def post_save_update_totals(sender, instance, created, *args, **kwargs):
    instance.cart.update_totals()

pre_save.connect(generate_cart_id, sender=Cart)
post_save.connect(post_save_update_totals, sender=CartProducts)
m2m_changed.connect(m2m_update_totals, sender=Cart.products.through)
