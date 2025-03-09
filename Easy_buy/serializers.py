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

class OrderItemSerializer(serializers.ModelSerializer):
    
    order_id = serializers.PrimaryKeyRelatedField(source = "order",queryset = Order.objects.all())
    product_id = serializers.PrimaryKeyRelatedField(source= "product",queryset = Product.objects.all())
    product_name = serializers.StringRelatedField(source="product")
    
    class Meta:
        model = OrderItem
        fields = ['id','order_id','product_id','product_name','quantity','total']

class DeliverySerializer(serializers.ModelSerializer):
    
    order_id = serializers.PrimaryKeyRelatedField(source = "order",queryset = Order.objects.all())
    deliverer_id = serializers.PrimaryKeyRelatedField(source= "delivery",queryset = User.objects.filter(role="delivery"))
    deliverer = serializers.StringRelatedField(source="delivery")
    
    class Meta:
        model = Delivery
        fields = ['id','order_id','deliverer_id','deliverer','status']