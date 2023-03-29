from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.



class ProfileUser(AbstractUser):
    email = models.CharField(max_length=100, unique=True)
    profile_pic = models.ImageField(default = 'images/generic-user-icon-13.jpg' ,upload_to='images/')
    mobile_no = models.CharField(max_length=15, null=True)
    p_address = models.CharField(max_length=200, null=True)
    dob = models.DateTimeField(null=True)
    country = models.CharField(max_length=20, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'username','first_name', 'last_name'] 


class Address(models.Model):
    user = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state  = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=200, null=True)
    pincode  = models.CharField(max_length=200)


class Tags(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

class Products(models.Model):
    product_name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', null=True)
    price = models.FloatField(max_length=50)
    tag = models.ManyToManyField(Tags, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    stock_available = models.CharField(max_length=200)

class Wishlist(models.Model):
    user  = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    product  = models.ForeignKey(Products, on_delete=models.CASCADE)




class Order(models.Model):
    user  = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    # product  = models.ForeignKey(Products, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price = models.CharField(max_length=200)
    ordered_date = models.DateTimeField(auto_now=True)

class Order_item(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    item_price = models.CharField(max_length=200)












