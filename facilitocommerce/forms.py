from django import forms
#from django.contrib.auth.models import User
from profiles.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(
        min_length=4, max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
        'class': 'form-control', 'id': 'username', 'placeholder': 'Username'
    }))

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
        'class': 'form-control', 'id': 'email', 'placeholder': 'Email'
    }))

    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'id': 'password', 'placeholder': 'Password'
    }))

    password2 = forms.CharField(
        label='Confirmar password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'id': 'password2', 'placeholder': 'Confirm password'
    }))

    #https://docs.djangoproject.com/en/2.2/ref/forms/validation/
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El username ya se encuentra en uso')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya se encuentra en uso')
        return email

    #Validar campos que dependan de otros
    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password') != cleaned_data.get('password'):
            self.add_error('password', 'El password no coincide')

    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )
