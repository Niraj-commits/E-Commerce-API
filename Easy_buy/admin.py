from django.contrib import admin
from .models import *

# Register your models here.
class orderitems(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [orderitems]


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Delivery)
admin.site.register(Purchase)
admin.site.register(Purchase_Item)
admin.site.register(PurchaseAccept)