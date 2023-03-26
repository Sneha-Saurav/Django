from django import forms 
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, ImageField, Textarea, DateInput
from .models import Products, Address, ProfileUser



class RegisterForm(forms.ModelForm):
     def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
     class Meta:
        model = ProfileUser
        fields =('first_name', 'last_name','username', 'password', 'email','mobile_no','dob', 'country')
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
                 }),
                  'first_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Username'
                }),
                 'last_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Username'
                }),
                 'mobile_no': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Username'
                }),
                 'dob': DateInput(attrs={'type': 'date',
                                         'class': "form-control",
                                        'placeholder': 'Username'}),

                 'country': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Username'
                }),
        }
    
class LoginForm(forms.ModelForm):
     class Meta:
        model = ProfileUser
        fields =('email', 'password')
        widgets = {
            'email': EmailInput(attrs={
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
                'description': Textarea(attrs={
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

class AddressForm(forms.ModelForm):
       class Meta:
        model = Address
        fields = ('address','state','mobile_no','pincode', 'shipping_address','city')
        widgets = {
            'address': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Address'
                }),
                'state': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'State'
                }),
                'mobile_no': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Mobile Number'
                }),
               'shipping_address': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Shiping Address '
                }),
                'pincode': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Pin code'
                }),
                'city': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'City'
                })
               
         }
        

class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields = '__all__'
        exclude  = ('is_superuser','is_staff','is_active', 'date_joined','last_login', 'password', 'profile_pic')
        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'firsr name'
                }),
                'last_name': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'last name '
                }),
                'username': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Username'
                }),
                'email': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'Email'
                }),
                'dob': DateInput(attrs={
                    'type':'date',
                'class': "form-control",
                'placeholder': 'Date of Birth '
                }),
                'country': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'country'
                }),
                'mobile_no': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'mobile no'
                }),
                'p_address': TextInput(attrs={
                'class': "form-control",
                'placeholder': 'p_address'
                }),

        }




class EditProfilePicForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        fields = ['profile_pic']
    
class ChangePassword(forms.ModelForm):
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ChangePassword, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    class Meta:
        model = ProfileUser
        fields = ['password']
        widgets = {
            'password': PasswordInput(attrs={
                'class': "form-control",
                'placeholder': 'password'
                }),

        }



           
    

        

    