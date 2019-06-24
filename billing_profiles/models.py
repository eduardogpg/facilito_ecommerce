from django.db import models
from profiles.models import User

from stripeAPI.card import create_card

class BillingProfile(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    token = models.CharField(max_length=50, null=True, blank=True)
    card_id = models.CharField(max_length=50, null=True, blank=True)
    last4 = models.CharField(max_length=4, null=True, blank=True)
    brand = models.CharField(max_length=10, null=True, blank=True)
    default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.card_id)

    @classmethod
    def create_by_stripe_token(cls, user, stripe_token):

        if user.customer_id and stripe_token:
            card = create_card(user, stripe_token)

            return user.billingprofile_set.create(card_id=card.id, last4=card.last4, brand=card.brand,
                                                  token=stripe_token,
                                                  default=not user.has_billing_profile())
