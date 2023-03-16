from django import forms 
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, ImageField
from .models import Products
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
     class Meta:
        model = User
        fields =('username', 'password', 'email')
        widgets = {
            'username': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Username'
                }),
            'email': EmailInput(attrs={
                'class': "form-control", 
                'placeholder': 'Email'
                }),
                 'password': PasswordInput(attrs={
                'class': "form-control", 
                'placeholder': 'Password'
                 })
        }
    
class LoginForm(forms.ModelForm):
     class Meta:
        model = User
        fields =('username', 'password')
        widgets = {
            'username': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Username'
                }),
           'password': PasswordInput(attrs={
                'class': "form-control", 
                'placeholder': 'Password'
                 })}
    

class Product_form(forms.ModelForm):
    class Meta:
        model = Products
        fields ='__all__'
        exclude = ['created_at']
        widgets = {
            'product_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Name'
                }),
                'description': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Description'
                }),
                'category': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'category'
                }),
                # 'image': ImageField(attrs={
                # 'class': "form-control",
                # }),
                'price': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'price'
                }),
                'stock_available': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'stock'
                })


        }
           
    

        

    