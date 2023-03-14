from django.db import models

# Create your models here.

class Products(models.Model):
    product_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    price = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now=True)
    stock_available = models.CharField(max_length=200)


# class Order(models.Model):
#     billing_Address = models.CharField(max_length=200)
#     shipping_address = models.CharField(max_length=200)
#     mobile_number = models.CharField(max_length=11)
#     payment_mode  = models.CharField(max_length=100)

class Cart(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

