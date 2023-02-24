from django.forms import ModelForm

from .models import Order, Customer

from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from django import forms

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['product_name', 'customer_name', 'status']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'profile_pic']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']