from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm (UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email','phone_number', 'first_name', 'last_name', 'password1', 'password2')

class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Email", required=True)