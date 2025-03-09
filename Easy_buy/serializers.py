from .models import *
from core.models import User
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class ProductSerializer(serializers.ModelSerializer):
    
    category = serializers.StringRelatedField()
    category_id = serializers.PrimaryKeyRelatedField(source = "category",queryset = Category.objects.all())
    
    class Meta:
        model = Product
        fields = ['id','name','category_id','category','price','description','quantity','available_status']

class OrderSerializer(serializers.ModelSerializer):
    
    customer_id = serializers.PrimaryKeyRelatedField(source = "customer",queryset = User.objects.filter(role="customer"))
    customer = serializers.StringRelatedField()
    
    class Meta:
        model = Order
        fields = ['id','customer_id','customer','status','created_at']