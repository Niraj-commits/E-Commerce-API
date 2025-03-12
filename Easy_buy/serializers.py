from .models import *
from core.models import User
from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class ProductSerializer(serializers.ModelSerializer):
    
    category = serializers.StringRelatedField()
    category_id = serializers.PrimaryKeyRelatedField(source = "category",queryset = Category.objects.all())
    creator = serializers.StringRelatedField(source = "created_by",read_only = True)
    
    class Meta:
        model = Product
        fields = ['id','name','category_id','category','price','description','quantity','available_status','creator']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        # self.context['request'].user gives the django user model instance of currently logged in user
        product = Product.objects.create(**validated_data)
        return product

class OrderItemSerializer(serializers.ModelSerializer):
    
    order_id = serializers.PrimaryKeyRelatedField(source = "order",queryset = Order.objects.all())
    product_id = serializers.PrimaryKeyRelatedField(source= "product",queryset = Product.objects.all())
    product_name = serializers.StringRelatedField(source="product")
    product_price = serializers.ReadOnlyField(source ="product.price") # fetching product price
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id','order_id','product_id','product_name',"product_price",'quantity','total']
    
    def get_total(self,order_item): #order_item is a declared variable
        return order_item.product.price * order_item.quantity #product here is Foreign_key name
    
class OrderSerializer(serializers.ModelSerializer):
    
    customer_id = serializers.PrimaryKeyRelatedField(source = "customer",queryset = User.objects.filter(role="customer"))
    customer = serializers.StringRelatedField()
    total_cost = serializers.SerializerMethodField()
    items = OrderItemSerializer(many =True)
    
    class Meta:
        model = Order
        fields = ['id','customer_id','customer','status','created_at','total_cost','items']
        
    def get_total_cost(self,order):
        total = 0
        for item in order.items.all(): #here items is related_field, set in FK of order items
            price =item.product.price
            quantity = item.quantity
            total += price *quantity
        return total
    
    def create(self, validated_data):
        items_list = validated_data.pop('items')        
        order = Order.objects.create(**validated_data)
        
        for item in items_list:
            OrderItem.objects.create(order = order,**item)
            #left order = FK, right order = created var above
        return order


class DeliverySerializer(serializers.ModelSerializer):
    
    order_id = serializers.PrimaryKeyRelatedField(source = "order",queryset = Order.objects.all())
    deliverer_id = serializers.PrimaryKeyRelatedField(source= "delivery",queryset = User.objects.filter(role="delivery"))
    deliverer = serializers.StringRelatedField(source="delivery")
    
    class Meta:
        model = Delivery
        fields = ['id','order_id','deliverer_id','deliverer','status']
    
    def create(self, validated_data):
        
        order = validated_data.get('order')
        status = validated_data.get('status')
        user = validated_data.get('delivery')
        duplicate_order = Delivery.objects.filter(order = order).exists()
        
        if duplicate_order:
            raise serializers.ValidationError("Record already exist")
        
        if order.status == "completed":
            raise serializers.ValidationError("Order is already completed")
        
        if status == "delivered":
            order.status = "completed"
            order.save()
        
        elif status == "assigned":
            order.status = "pending"
            order.save()
            
            send_mail(
                subject="Delivery Assigned",
                message= f"Hi {user.username}, A new delivery has been assigned to you.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list= [user.email],
            )
        
        elif status == "cancelled":
            order.status = "cancelled"
            order.save()
            delivery_entry = Delivery.objects.create(**validated_data)
            raise serializers.ValidationError("Sorry!! Order got cancelled")
        delivery_entry = Delivery.objects.create(**validated_data)
        return delivery_entry
        
    
    def update(self,instance,validated_data):
        order = validated_data.get('order')
        status = validated_data.get('status')
        delivery = validated_data.get('delivery')
        occurence = Delivery.objects.filter(order = order,delivery = delivery,status = status).exists()
        
        if instance.status == "cancelled":
            raise serializers.ValidationError("Cannot update order has been cancelled.")
        
        if instance.status == "delivered":
            raise serializers.ValidationError("Cannot update order has been delivered.")
        
        if occurence:
            raise serializers.ValidationError("Record already exist")
        
        if order.status == "completed":
            raise serializers.ValidationError("Order is already completed")
        
        if status == "delivered":
            order.status = "completed"
            order.save()
        
        elif status == "assigned":
            order.status = "pending"
            order.save()
        
        elif status == "cancelled":
            raise serializers.ValidationError("Order has been cancelled")
        instance.order = order
        instance.status = status
        instance.delivery = delivery
        instance.save()
        return instance
            
            