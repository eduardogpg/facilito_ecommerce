from django.db import models
from django.db.models import Q
from stripeAPI.customer import create_customer
from django.contrib.auth.models import AbstractUser

from orders.common import OrderStatus

#https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#extending-the-existing-user-model
class User(AbstractUser):
    customer_id = models.CharField(max_length=100, blank=True, null=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def shipping_address(self):
        return self.shippingaddress_set.filter(default=True).first()

    @property
    def billing_profile(self):
        return self.billingprofile_set.filter(default=True).first()

    @property
    def description(self):
        return 'Customer for {}'.format(self.email)

    def has_address(self):
        return self.shipping_address is not None

    def has_billing_profile(self):
        return self.billing_profile is not None

    def create_customer_id(self):
        if not self.customer_id:
            customer = create_customer(self)
            self.customer_id = customer.id
            self.save()

        return self.customer_id

class Customer(User):
    class Meta:
        proxy = True

    @classmethod
    def is_customer(self, user):
        return user.order_set.filter( Q(status=OrderStatus.PAYED)
                                    | Q(status=OrderStatus.COMPLETED)).count() > 0

    @classmethod
    def get_customer(self, user):
        if Customer.is_customer(user):
            return Customer.objects.get(pk=user.pk)

    def orders_completed(self):
        return self.order_set.filter(status=OrderStatus.COMPLETED).order_by('id')

    def orders_canceled(self):
        return self.order_set.filter(status=OrderStatus.CANCELED).order_by('id')
