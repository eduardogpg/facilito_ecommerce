from . import stripe

def create_customer(user):
    if not user.customer_id:
        customer = stripe.Customer.create(
            description="Customer for {}".format(user.email),
        )
        user.customer_id = customer.id
        user.save()

    return user.customer_id
