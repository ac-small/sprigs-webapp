import datetime

from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=500)
    merchant = models.CharField(max_length=400)
    flyer_id = models.CharField(max_length=200)
    price_units = models.CharField(max_length=200)
    sale_price = models.CharField(max_length=50)
    start_date = models.DateTimeField('start date')
    end_date = models.DateTimeField('end date')
    def __str__(self):
        return self.product_name
        
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=200)
    def __str__(self):
        return self.category
        
class Product_Classification(models.Model):
    id = models.AutoField(primary_key=True)
    classification = models.CharField(max_length=200)
    def __str__(self):
        return self.classification