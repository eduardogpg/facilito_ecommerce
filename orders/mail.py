from django.urls import reverse # returns a string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

class Mail:

    @staticmethod
    def get_absolute_url(url):
        return 'http://localhost:8000{}'.format(reverse(url))

    @staticmethod
    def send_complete_order_mail(order, user):
        subject = 'Tu pedido CodigoFacilito.com ha sido enviado'
        template = get_template('orders/mails/complete.html')
        content = template.render({
            'user': user,
            'order': order,
            'url': Mail.get_absolute_url('my_orders')
        })

        message = EmailMultiAlternatives(subject,
                                        'Mensaje importante',
                                         settings.EMAIL_HOST_USER,
                                         [user.email])

        message.attach_alternative(content, 'text/html')
        message.send()
