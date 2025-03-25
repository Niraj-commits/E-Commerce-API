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
            "name":['exact','icontains'],
            "category":['exact'],
        }