from django.forms import ModelForm
from .models import ShippingAddress

class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress

        fields = ['line1', 'line2', 'city', 'state',  'country', 'postal_code' ,'reference']
        labels = {  'line1': 'Calle 1',
                    'line2': 'Calle 2',
                    'city': 'Ciudad',
                    'state': 'Estado',
                    'country': 'País',
                    'postal_code': 'Código postal',
                    'reference': 'Referencias'
                 }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['line1'].widget.attrs.update({
            'class': 'form-control',
            'id': 'line1',
        })

        self.fields['line2'].widget.attrs.update({
            'class': 'form-control',
            'id': 'line2',
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

        self.fields['postal_code'].widget.attrs.update({
            'class': 'form-control',
            'id': 'postal_code',
            'placeholder': '0000'
        })

        self.fields['reference'].widget.attrs.update({
            'class': 'form-control',
            'id': 'zip',
            'placeholder': 'Referencias nos ayudan a encontrar tu ubicación'
        })
