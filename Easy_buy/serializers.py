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
    
    class Meta:
        model = Product
        fields = ['id','name','category_id','category','price','description','quantity','available_status']
    
    def create(self, validated_data):
        product = Product.objects.create(**validated_data)
        
        if product.quantity <5:
            self.mail_when_low_stock(product)
        
        return product
    def mail_when_low_stock(self,product):
        suppliers = User.objects.filter(role="supplier").values_list("email", flat=True)
        
        if suppliers:
            send_mail(
                subject="Stock is Running Low",
                message=f"The {product.name} is running low. Please Restock",
                from_email= settings.EMAIL_HOST_USER,
                recipient_list= list(suppliers)
            )

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



# For Creating Delivery

class DeliveryCreateSerializer(serializers.ModelSerializer):
    
    order_id = serializers.PrimaryKeyRelatedField(source = "order",queryset = Order.objects.all())
    deliverer_id = serializers.PrimaryKeyRelatedField(source= "delivery",queryset = User.objects.filter(role="delivery"))
    deliverer = serializers.StringRelatedField(source="delivery")
    status = serializers.CharField(read_only = True)
    
    class Meta:
        model = Delivery
        fields = ['id','order_id','deliverer_id','deliverer','status']
    
    def create(self, validated_data):
        
        order = validated_data.get('order')
        user = validated_data.get('delivery')
        duplicate_order = Delivery.objects.filter(order = order).exists()
        
        if duplicate_order:
            raise serializers.ValidationError("Record already exist")
        
        if order.status == "delivered":
            raise serializers.ValidationError("Order is already completed")
            
        validated_data['status'] = 'assigned'
        order.status = "pending"
        order.save()
            
        send_mail(
            subject="Delivery Assigned",
            message= f"Hi {user.username}, A new delivery has been assigned to you.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list= [user.email],
            )
        
        delivery_entry = Delivery.objects.create(**validated_data)
        return delivery_entry 

# For Updating Deleting Delivery Details 

class DeliveryUpdateSerializer(serializers.ModelSerializer):
    order_id = serializers.PrimaryKeyRelatedField(source = "order",queryset = Order.objects.all())
    deliverer_id = serializers.PrimaryKeyRelatedField(source= "delivery",queryset = User.objects.filter(role="delivery"))
    deliverer = serializers.StringRelatedField(source="delivery")
    
    class Meta:
        model = Delivery
        fields = ['id','order_id','deliverer_id','deliverer','status']

    def update(self,instance,validated_data):
        self.fields['status'].read_only = False
        order = validated_data.get('order')
        status = validated_data.get('status')
        user = validated_data.get('delivery')
        occurence = Delivery.objects.filter(order = order,delivery = user,status = status).exists()
        
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
            
            for item in order.items.all():
                if item.product.quantity < item.quantity:
                    raise serializers.ValidationError(f"Not enough quantities for {item.product.name}")
                item.product.quantity -= item.quantity
                item.product.save()
            order.save()
            
            send_mail(
                subject="Delivery Assigned",
                message= f"Hi {user.username} delivery has been completed please recieve the package.",
                from_email=user.email,
                recipient_list= [order.customer.email],
            )
        
        elif status == "cancelled":
            instance.status = "cancelled"
            order.status = "cancelled"
            order.save()
            instance.save()
            send_mail(
                subject="Delivery Cancelled",
                message= f"Hi {user.username} delivery has been cancelled please contact seller for further information.",
                from_email=user.email,
                recipient_list= [order.customer.email],
            )
            raise serializers.ValidationError("Order has been cancelled")
        instance.order = order
        instance.status = status
        instance.delivery = user
        instance.save()
        return instance
            
class PurchaseSerializer(serializers.ModelSerializer):
    
    supplier = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.filter(role = "supplier")
    )
    price = serializers.ReadOnlyField(source = "product.price")
    total_cost = serializers.SerializerMethodField()
    
    class Meta:
        model = Purchase
        fields = ['id','supplier','product',"price",'quantity','total_cost']

    def get_total_cost(self,purchase):
        return purchase.product.price * purchase.quantity
    
    def create(self, validated_data):
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        
        product.quantity += quantity
        product.save()
        
        purchase = Purchase.objects.create(**validated_data)
        return purchase