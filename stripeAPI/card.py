from . import stripe

def create_card(user, token):
    """
    Los clientes también pueden almacenar múltiples métodos de pago.
    El primero guardado es el que se define como default_sourcedel cliente.
    Este se utiliza para los pagos de suscripciones y cuando se solicite un pago solo con el ID del cliente.
    """

    try:
        card = stripe.Customer.create_source(user.customer_id, source=token)

        return user.billingprofile_set.create(card_id=card.id,
                                                last4=card.last4,
                                                brand=card.brand,
                                                default=not user.has_billing_profile())

    except stripe.error.InvalidRequestError as e:
        print("Ha ocurrido un error al crear un nuevo método de pago.")
        return None
