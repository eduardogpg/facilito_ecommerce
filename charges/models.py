from django.db import models

from orders.models import Order
from profiles.models import User

from stripeAPI.charge import create_charge

class Charge(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    charge_id = models.CharField(max_length=50)
    amount = models.IntegerField()
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.charge_id

    @classmethod
    def create_charge_by_order(cls, order):
        if order.billing_profile_id and order.user_id:
            charge = create_charge(order)

            if charge.status == 'succeeded':
                charge = Charge.objects.create(user=order.user, order=order,
                                               charge_id=charge.id, amount=charge.amount,
                                               payment_method=charge.payment_method,
                                               status=charge.status)
                order.payed()
                return charge
