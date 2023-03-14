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



