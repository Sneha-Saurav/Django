from django import forms
from .models import Products


class RegisterForm(forms.Form):
    username = forms.CharField(label="Enter the username", max_length=50)
    password =forms.CharField(max_length=20, widget=forms.PasswordInput)

class Product_form(forms.ModelForm):
    class Meta:
        model = Products
        fields ='__all__'
        exclude = ['created_at']

        

    