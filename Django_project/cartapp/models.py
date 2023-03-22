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

class Cart(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    product  = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity  = models.IntegerField()


class Order(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    product  = models.ForeignKey(Products, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=200)
    total_price = models.CharField(max_length=200)
    Mobile_number = models.CharField(max_length=11)
    ordered_date = models.DateTimeField(auto_now=True)







