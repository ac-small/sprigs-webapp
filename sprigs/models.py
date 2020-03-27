import datetime

from django.db import models

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(default=None, blank=True, null=True, max_length=500)
    merchant = models.CharField(default=None, blank=True, null=True, max_length=400)
    flyer_id = models.CharField(default=None, blank=True, null=True, max_length=200)
    price_units = models.CharField(default=None, blank=True, null=True, max_length=200)
    sale_price = models.CharField(default=None, blank=True, null=True, max_length=50)
    start_date = models.DateTimeField('start date', default=None, blank=True, null=True)
    end_date = models.DateTimeField('end date', default=None, blank=True, null=True)
    def __str__(self):
        return self.product_name
        
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(default=None, blank=True, null=True, max_length=200)
    def __str__(self):
        return self.category
        
class Product_Classification(models.Model):
    id = models.AutoField(primary_key=True)
    product_id = models.IntegerField(default=None, blank=True, null=True)
    classification = models.CharField(default=None, blank=True, null=True, max_length=200)
    def __str__(self):
        return self.classification