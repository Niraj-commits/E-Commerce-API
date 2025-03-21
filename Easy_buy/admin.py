from django.contrib import admin
from .models import *

# Register your models here.
class orderitems(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [orderitems]

class purchaseItems(admin.TabularInline):
    model = Purchase_Item
    extra = 0

class PurchaseAdmin(admin.ModelAdmin):
    inlines = [purchaseItems]

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(OrderDelivery)
admin.site.register(Purchase,PurchaseAdmin)
admin.site.register(Purchase_Item)
admin.site.register(PurchaseDelivery)