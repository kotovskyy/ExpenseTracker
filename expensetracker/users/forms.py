from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class CustomPasswordInput(forms.PasswordInput):
    def __init__(self, attrs=None, render_value=False):
        super().__init__(attrs={'class': 'auth-form-field',
                                'placeholder': 'password...'})

class SignupForm(UserCreationForm):
    password1 = forms.CharField(widget=CustomPasswordInput)
    password2 = forms.CharField(widget=CustomPasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'auth-form-field',
                                               'placeholder': 'username...'}),
            'email': forms.EmailInput(attrs={'class': 'auth-form-field',
                                             'placeholder': 'email...'}),
        }
