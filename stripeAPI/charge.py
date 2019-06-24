from . import stripe

def create_charge(user, order):
    return stripe.Charge.create(
        amount=order.total,
        currency='USD',
        description=order.description,
        source=order.billing_profile.card_id, #A payment source to be charged. This can be the ID of a card
    )
