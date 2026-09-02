from django import forms
from .models import Order
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User 

class OrderForm(forms.ModelForm):
    class Meta:
        model= Order
        fields= ['quantity', 'address','payment_method'] 


class Registeration(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']


class LoginForm(AuthenticationForm):
    pass           