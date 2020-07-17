from django import forms
from .models import Product, Customer
from django.contrib.auth.models import User

# class UserForm(forms.ModelForm):
#      class Meta:
#           model = User
#           fields = [
#                'username', 'first_name', 'last_name', 'password', 'password'
#           ]
     
class CustomerForm(forms.ModelForm):
     class Meta:
          model = Customer
          fields = [
               'name'
          ]