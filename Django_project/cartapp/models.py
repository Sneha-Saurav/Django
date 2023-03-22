from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Products(models.Model):
    product_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    price = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    stock_available = models.CharField(max_length=200)

class Wishlist(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    product  = models.ForeignKey(Products, on_delete=models.CASCADE)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    state  = models.CharField(max_length=200)
    mobile_no = models.CharField(max_length=200)
    pincode  = models.CharField(max_length=200)


class Order(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    product  = models.ForeignKey(Products, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    total_price = models.CharField(max_length=200)
    ordered_date = models.DateTimeField(auto_now=True)







