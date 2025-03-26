from django_filters import rest_framework as filter
from .models import *

class CategoryFilter(filter.FilterSet):
    class Meta:
        model  = Category
        fields = {
            "name":['exact'],
        }

class ProductFilter(filter.FilterSet):
    
    category = filter.CharFilter(field_name="category__name",lookup_expr="icontains")
    
    class Meta:
        model = Product
        fields = {
            "name":['icontains'],
            "category":['exact'],
            "price":["gte","lte"]
        }

class OrderFilter(filter.FilterSet):
    
    customer = filter.CharFilter(field_name="customer__username",lookup_expr="icontains")
    
    class Meta:
        model = Order
        fields = {
            "status":['exact'],
            "customer":['exact'], 
                  }

class OrderDeliveryFilter(filter.FilterSet):
    
    delivery = filter.CharFilter(field_name="delivery__username",lookup_expr="icontains")
    
    class Meta:
        model = OrderDelivery
        fields = {
            "delivery":["exact"],
            "status":['exact'],
        }

class PurchaseFilter(filter.FilterSet):
    
    supplier = filter.CharFilter(field_name="supplier__username",lookup_expr="icontains")
    
    class Meta:
        model = Purchase
        fields = {
            "supplier":['exact'],
            "status":['exact'],
                  }

class PurchaseDeliveryFilter(filter.FilterSet):
    
    delivery = filter.CharFilter(field_name="delivery__username",lookup_expr="icontains")
    
    class Meta:
        model = PurchaseDelivery
        fields = {
            "delivery":["exact"],
            "status":['exact'],
        }