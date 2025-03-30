from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.

class CustomUser(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password','role','address','phone','company_name','vehicle_type','license_no')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password','role','address','phone','company_name','vehicle_type','license_no'),
        }),
    )
    list_display = ['id','username','role']
    list_editable = ['role']
    list_filter = ['role']
    search_fields = ['role','username']
    list_per_page = 10

admin.site.register(User,CustomUser)