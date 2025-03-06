from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUser(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password','role','address','phone','vehicle_type','company_name','availability_status')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password','role','address','phone','vehicle_type','company_name','availability_status'),
        }),
    )

admin.site.register(User,CustomUser)