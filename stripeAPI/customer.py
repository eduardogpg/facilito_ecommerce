import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_customer(user):
    if not user.customer_id:
        customer = stripe.Customer.create(
            description="Customer for {}".format(user.email),
        )
        user.customer_id = customer.id
        user.save()

    return user.customer_id

def create_card(user, token):
    try:
        card = stripe.Customer.create_source(user.customer_id, source=token)

        return user.billingprofile_set.create(card_id=card.id,
                                                last4=card.last4,
                                                brand=card.brand,
                                                default=not user.has_billing_profile)

    except stripe.error.InvalidRequestError as e:
        print("Ha ocurrido un error al crear un nuevo método de pago.")
        return None
