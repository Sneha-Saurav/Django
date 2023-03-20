from django import forms
from .models import Blog
from django.contrib.auth.models import User


class BlogForm(forms.ModelForm):
    class Meta:
        model  = Blog
        fields ='__all__'
        exclude = ['is_published']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields  = '__all__'

        
class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
