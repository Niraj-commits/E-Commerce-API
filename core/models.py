from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'admin'),
        ('supplier', 'supplier'),
        ('customer', 'customer'),
        ('delivery_person', 'delivery_person'),
    ]
    vehicle_choices = [('scooter','scooter'),('bike','bike')]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    address = models.CharField(max_length=255,default="ktm")
    phone = models.CharField(max_length=15)
    company_name = models.CharField(max_length=25,blank=True,null=True)
    vehicle_type = models.CharField(max_length=25,choices=vehicle_choices,default='bike',null=True,blank=True)
    license_no = models.CharField(max_length=16,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.username

