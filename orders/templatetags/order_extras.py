from django import template

register = template.Library()

@register.filter()
def order_format(value):
    return '{} {}'.format(value, 'pedidos' if value > 1 else 'pedido')
