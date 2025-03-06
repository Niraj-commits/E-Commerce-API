from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    role_choices = [('admin','admin'),('supplier','supplier'),('customer','customer'),('delivery','delivery')]
    
    address = models.CharField(max_length=25,blank=True,null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    vehicle_type = models.CharField(max_length=25,null=True,blank=True)
    company_name = models.CharField(max_length=25,null=True,blank=True)
    availability_status = models.BooleanField(default=True,null=True,blank=True)
    role = models.CharField(max_length=25,choices=role_choices,default='customer')
    created_at = models.DateTimeField( auto_now_add=True)
    
    