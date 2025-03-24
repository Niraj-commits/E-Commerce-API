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
    
    def __str__(self):
        return self.name

class Order(models.Model):  
    status_options = [('pending','pending'),('delivered','delivered'),('cancelled','cancelled')]
    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name="order_set")
    status = models.CharField(max_length=25,choices=status_options,default="pending")
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return (f"Ordered By: {self.customer.username},Order No: {self.id}")

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return (f"Order: {self.order},product: {self.product.name}")

class OrderDelivery(models.Model):
    status_choices = [('assigned','assigned'),('delivered','delivered'),('cancelled','cancelled')]
    
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    delivery = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=25,choices=status_choices,default="assigned")

class Purchase(models.Model):
    
    order_status = [('pending','pending'),('accepted','accepted'),('cancelled','cancelled')]
    supplier = models.ForeignKey(User,on_delete=models.CASCADE,related_name="purchase_set")
    status = models.CharField(max_length=25,choices=order_status,default="pending")

class Purchase_Item(models.Model):
    
    purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE,related_name="add_items")
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class PurchaseDelivery(models.Model):
    status_choices = [('pending','pending'),('delivered','delivered'),('cancelled','cancelled')]
    
    purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE)
    delivery = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=25,choices=status_choices,default="pending")

