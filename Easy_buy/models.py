from django.db import models
from core.models import *

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=25)
    
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    available_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()

class Order(models.Model):  
    status_options = [('pending','pending'),('delivered','delivered'),('cancelled','cancelled')]
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=25,choices=status_options,default="pending")
    created_at = models.DateField(auto_now_add=True)

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