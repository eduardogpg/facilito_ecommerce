from django.forms import ModelForm
from .models import ShippingAddress

class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'state',  'country', 'zip' ,'reference']
        labels = {  'address': 'Calle',
                    'city': 'Ciudad',
                    'state': 'Estado',
                    'country': 'País',
                    'zip': 'Código postal',
                    'reference': 'Referencias' }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['address'].widget.attrs.update({
            'class': 'form-control',
            'id': 'address',
        })

        self.fields['city'].widget.attrs.update({
            'class': 'form-control',
            'id': 'city',
        })

        self.fields['state'].widget.attrs.update({
            'class': 'form-control',
            'id': 'state',
        })

        self.fields['country'].widget.attrs.update({
            'class': 'form-control',
            'id': 'country',
        })

        self.fields['zip'].widget.attrs.update({
            'class': 'form-control',
            'id': 'zip',
            'placeholder': '0000'
        })

        self.fields['reference'].widget.attrs.update({
            'class': 'form-control',
            'id': 'zip',
            'placeholder': 'Referencias nos ayudan a encontrar tu ubicación'
        })
