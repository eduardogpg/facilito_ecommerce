from django.forms import ModelForm
from .models import BillingProfile

class BillingProfileForm(ModelForm):
    class Meta:
        model = BillingProfile
        fields = ['streat', 'state', 'phone', 'zip' ,'reference']
        labels = {'streat': 'Calle', 'state': 'Estado', 'phone': 'Telefono', 'zip': 'Código postal' }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['streat'].widget.attrs.update({
            'class': 'form-control',
            'id': 'streat',
        })

        self.fields['state'].widget.attrs.update({
            'class': 'form-control',
            'id': 'state',
        })

        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'id': 'phone',
        })

        self.fields['streat'].widget.attrs.update({
            'class': 'form-control',
            'id': 'streat',
        })

        self.fields['reference'].widget.attrs.update({
            'class': 'form-control',
            'id': 'reference',
            'placeholder': 'Referencias nos ayudan a encontrar tu ubicación'
        })

        self.fields['zip'].widget.attrs.update({
            'class': 'form-control',
            'id': 'zip',
            'placeholder': '0000'
        })
