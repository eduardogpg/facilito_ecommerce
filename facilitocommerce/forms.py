from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'username', 'placeholder': 'username'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'id': 'email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'id': 'password'
    }))

    def clean_email(self):
        email = self.cleaned_data.get('username')
        if not email.endswith('gmail.com'):
            raise forms.ValidationError('El correo debe ser gmail')

        return email
