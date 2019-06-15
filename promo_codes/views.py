from django.shortcuts import render
from django.http import JsonResponse

from .models import PromoCode
from orders.utils import get_order

def validate(request):
    order = get_order(request)
    promo_code = PromoCode.objects.get_valid(request.GET.get('code'))

    if promo_code is None or order is None:
        return JsonResponse({'status': False}, status=404)

    order.apply_promo_code(promo_code)

    return JsonResponse({
        'status': True,
        'code': promo_code.code,
        'discount': promo_code.discount,
        'total': order.total
    })
