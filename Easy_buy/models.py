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
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    price = models.FloatField()
    
    def __str__(self):
        return self.name

# class Cart(models.Model):
#     customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name="customer")
    
# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
#     product = models.ForeignKey(Product,on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
    
#     def __str__(self):
#         return (f"cart: {self.cart},product: {self.product.name}")

class Order(models.Model):  
    status_options = [('pending','pending'),('delivered','delivered'),('cancelled','cancelled')]
    customer = models.ForeignKey(User,on_delete=models.CASCADE,related_name="customer")
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

class Delivery(models.Model):
    status_choices = [('assigned','assigned'),('delivered','delivered'),('cancelled','cancelled')]
    
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    delivery = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=25,choices=status_choices,default="assigned")

class Purchase(models.Model):
    supplier = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()