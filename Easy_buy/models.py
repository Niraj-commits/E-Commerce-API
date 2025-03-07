from django.db import models
from core.models import *

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)


class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    available_status = models.BooleanField(default=True)
    supplier = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()

class Order(models.Model):
    
    status_options = [('pending','pending'),('delivered','delivered'),('cancelled','cancelled')]
    
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    total = models.FloatField()
    status = models.CharField(max_length=25,choices=status_options,default="pending")
    created_at = models.DateTimeField(auto_created=True)

class OrderItem(models.Model):
    
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.FloatField()
    price = models.FloatField()

class Delivery(models.Model):
    status_choices = [('assigned','assigned'),('in_progress','in_progress'),('delivered','delivered')]
    
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    delivery = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=25,choices=status_choices,default="assigned")
    estimate_delivery_date = models.DateTimeField(auto_now=False,auto_now_add=False)
    actual_delivery_date = models.DateTimeField(null=True,blank=True)

class Notification(models.Model):
    
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Dashboard(models.Model):
    
    total_revenue = models.FloatField()
    top_products = models.CharField(max_length=25)
    total_orders = models.IntegerField()