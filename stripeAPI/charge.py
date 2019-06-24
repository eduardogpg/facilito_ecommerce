from . import stripe

def create_charge(order):
    if order.billing_profile_id and order.user_id:
        return stripe.Charge.create(
            amount=int(order.total * 100),
            currency='USD',
            description=order.description,
            customer=order.user.customer_id,
            source=order.billing_profile.card_id, #A payment source to be charged. This can be the ID of a card
            metadata={
                'order_id': order.id
            }
        )
