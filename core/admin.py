from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUser(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password','role','address','phone','company_name','vehicle_type','license_no','availability_status')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password','role','address','phone','company_name','vehicle_type','license_no','availability_status'),
        }),
    )

admin.site.register(User,CustomUser)