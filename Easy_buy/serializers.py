from .models import *
from core.models import User
from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']
        
    def create(self,validated_data):
        
        duplicate = self.Meta.model.objects.filter(name = validated_data.get('name')).exists()
        if duplicate:
            raise serializers.ValidationError("Category with that name already exist")
        category = Category.objects.create(**validated_data)
        return category
    
    def update(self,instance,validated_data):
        
        duplicate = self.Meta.model.objects.filter(name = validated_data.get('name')).exists()
        if duplicate:
            raise serializers.ValidationError("Category with that name already exist.Cannot update")
        
        instance.name = validated_data.get('name')
        instance.save()
        return instance
        
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
    
    product_id = serializers.PrimaryKeyRelatedField(source= "product",queryset = Product.objects.all())
    product_name = serializers.StringRelatedField(source="product")
    product_price = serializers.ReadOnlyField(source ="product.price") # fetching product price
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id','product_id','product_name',"product_price",'quantity','total']
    
    def get_total(self,order_item): #order_item is a declared variable
        return order_item.product.price * order_item.quantity #product here is Foreign_key name
    
    def create(self,validated_data):
        
        occurence = OrderItem.objects.filter(product = validated_data.get('product'),order = validated_data.get('order')).exists()
        if occurence:
            raise serializers.ValidationError("Error: Order Item already exist in this order")
        order_item = OrderItem.objects.create(**validated_data)
        return order_item
    
    def update(self,instance,validated_data):
        
        instance.product = validated_data.get('product')
        instance.quantity = validated_data.get('quantity')
        instance.save()
        return instance
    
class OrderSerializer(serializers.ModelSerializer):
    
    customer = serializers.HiddenField(default = serializers.CurrentUserDefault())
    customer_name = serializers.StringRelatedField(source = "customer")
    total_cost = serializers.SerializerMethodField()
    items = OrderItemSerializer(many =True)
    
    class Meta:
        model = Order
        fields = ['id','customer','customer_name','status','total_cost','items']
        
    def get_total_cost(self,order):
        total = 0
        for item in order.items.all(): #here items is related_field, set in FK of order items
            price =item.product.price
            quantity = item.quantity
            total += price *quantity
        return total
    
    def create(self, validated_data):
        
        items_list = validated_data.pop('items')    #To create order we need to pop items              
        order = Order.objects.create(**validated_data)
        
        for item in items_list:
            OrderItem.objects.create(order = order,**item)
            #left order = FK, right order = created var above
        return order
    
    def update(self,instance,validated_data):
        items_list = validated_data.pop('items')
        
        instance.status = validated_data.get('status')
        instance.save()
        return instance

class OrderDeliverySerializer(serializers.ModelSerializer):
    
    order_id = serializers.PrimaryKeyRelatedField(source = "order",queryset = Order.objects.all())
    deliverer_id = serializers.PrimaryKeyRelatedField(source= "delivery",queryset = User.objects.filter(role="delivery"))
    deliverer = serializers.StringRelatedField(source="delivery")
    
    class Meta:
        model = OrderDelivery
        fields = ['id','order_id','deliverer_id','deliverer','status']
    
    def create(self, validated_data):
        
        order = validated_data.get('order')
        user = validated_data.get('delivery')
        status = validated_data.get('status')
        duplicate_order = OrderDelivery.objects.filter(order = order).exists()
        
        if duplicate_order:
            raise serializers.ValidationError("Record already exist")
        
        if order.status == "delivered":
            raise serializers.ValidationError("Order is already completed")
        
        if order.status == "cancelled":
            raise serializers.ValidationError("Order has been cancelled")
        
        if status == "assigned":   
            order.status = "pending"
            order.save()
            send_mail(
                subject="Order Delivery Assigned",
                message= f"hi {user.username} a new delivery has been assigned to you",
                from_email= order.customer.email,
                recipient_list=[user.email]
            )
        
        elif status == "cancelled":
            order.status = "cancelled"
            order.save()
            send_mail(
                subject="Delivery Cancelled",
                message= f"Order delivery has been cancelled.",
                from_email=user.email,
                recipient_list= [order.customer.email],
                )
        
        elif status == "completed":
            order.status = "delivered"
            order.save()
            
            for item in order.items.all():
                if item.product.quantity < item.quantity:
                    raise serializers.ValidationError(f"Not enough quantities for {item.product.name}")
                item.product.quantity -= item.quantity
                item.product.save()
                
            send_mail(
                subject="Order Completed",
                message= f"hi {order.customer.username} delivery has been completed",
                from_email=user.email,
                recipient_list= [order.customer.email],
            )
        
        delivery_entry = OrderDelivery.objects.create(**validated_data)
        return delivery_entry 

    def update(self,instance,validated_data):
        order = validated_data.get('order')
        status = validated_data.get('status')
        user = validated_data.get('delivery')
        occurence = OrderDelivery.objects.filter(order = order,delivery = user,status = status).exists()
        
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
                subject="Order Completed",
                message= f"hi {order.customer.username} delivery has been completed",
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
                message= f"Order delivery has been cancelled.",
                from_email=user.email,
                recipient_list= [order.customer.email],
                )
            raise serializers.ValidationError("Order has been cancelled")
        instance.order = order
        instance.status = status
        instance.delivery = user
        instance.save()
        return instance
            
class PurchaseItemSerializer(serializers.ModelSerializer):
    
    product_name = serializers.StringRelatedField(source="product")
    price = serializers.ReadOnlyField(source = "product.price")
    total_cost = serializers.SerializerMethodField()
    
    
    class Meta:
        model = Purchase_Item
        fields = ['id','product_name','product',"price",'quantity','total_cost']

    def get_total_cost(self,purchase):
        return purchase.product.price * purchase.quantity
    
    def create(self, validated_data):
        occurence = OrderItem.objects.filter(product = validated_data.get('product'),order = validated_data.get('order')).exists()
        if occurence:
            raise serializers.ValidationError("Error: Purchase Item already exist in this order")
        
        purchase = Purchase.objects.create(**validated_data)
        return purchase
    
    def update(self,instance,validated_data):
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')
        
        instance.product = product
        instance.quantity = quantity
        instance.save()
        return instance

class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(many = True)
    supplier_name = serializers.StringRelatedField(source = "supplier")
    supplier = serializers.HiddenField(default = serializers.CurrentUserDefault())
    total = serializers.SerializerMethodField()
    
    class Meta:
        model = Purchase
        fields = ['id','supplier','supplier_name','status','status',"total",'items']
    
    def get_total(self,purchase):
        total = 0
        for item in purchase.items.all(): #here items is related_field, set in FK of purchase items
            price =item.product.price
            quantity = item.quantity
            total += price *quantity
        return total
    
    def create(self, validated_data):
        
        items_list = validated_data.pop('items')
        purchase = Purchase.objects.create(**validated_data)
        
        for item in items_list:
            Purchase_Item.objects.create(purchase = purchase,**item)
        return purchase
    
    def update(self,instance,validated_data):
        
        items_list = validated_data.pop('items')
        
        instance.status = validated_data.get('status')
        instance.save()
        return instance

class PurchaseDeliverySerializer(serializers.ModelSerializer):
    
    purchase_id = serializers.PrimaryKeyRelatedField(source = "purchase",queryset = Purchase.objects.all())
    deliverer_id = serializers.PrimaryKeyRelatedField(source= "delivery",queryset = User.objects.filter(role="delivery"))
    deliverer = serializers.StringRelatedField(source="delivery")
    
    class Meta:
        model = PurchaseDelivery
        fields = ['id','purchase_id','deliverer_id','deliverer','status']
    
    def create(self, validated_data):
        
        status = validated_data.get('status')
        purchase = validated_data.get('purchase')
        user = validated_data.get('delivery')
        duplicate_purchase = PurchaseDelivery.objects.filter(purchase = purchase,delivery = user).exists()
        
        if duplicate_purchase:
            raise serializers.ValidationError("Record already exist")
        
        if Purchase.status == "delivered":
            raise serializers.ValidationError("Purchase is already completed")
        
        if Purchase.status == "cancelled":
            raise serializers.ValidationError("Purchase is cancelled")
        
        if status == "assigned":
            purchase.status = "pending"
            purchase.save()
            
            
            send_mail(
                subject="Purchase Delivery Assigned",
                message= f"hi {user.username} a new delivery has been assigned to you",
                from_email= purchase.supplier.email,
                recipient_list=[user.email]
            )
        
        elif status == "delivered":
            purchase.status = "delivered"
            purchase.save()
            
            for item in purchase.items.all():
                item.product.quantity += item.quantity
                item.product.save() 
            
            send_mail(
                subject="Purchase Delivered",
                message= f"hi {purchase.supplier.username} delivery has been completed",
                from_email=user.email,
                recipient_list= [purchase.supplier.email],
            )
            
        elif status == "cancelled":
            purchase.status = "cancelled"
            purchase.save()
            send_mail(
                subject="Delivery Cancelled",
                message= f"purchase delivery has been cancelled.",
                from_email=user.email,
                recipient_list= [purchase.supplier.email],
                )
        
        delivery_entry = PurchaseDelivery.objects.create(**validated_data)
        return delivery_entry 

    def update(self,instance,validated_data):
        purchase = validated_data.get('purchase')
        status = validated_data.get('status')
        user = validated_data.get('delivery')
        occurence = PurchaseDelivery.objects.filter(purchase = purchase,delivery = user,status = status).exists()
        
        if instance.status == "cancelled":
            raise serializers.ValidationError("Cannot update order has been cancelled.")
        
        if instance.status == "delivered":
            raise serializers.ValidationError("Cannot update order has been delivered.")
        
        if occurence:
            raise serializers.ValidationError("Record already exist")
        
        if purchase.status == "delivered":
            raise serializers.ValidationError("Purchase is already completed")
        
        if status == "delivered":
            purchase.status = "completed"
            purchase.save()
            
            for item in purchase.items.all():
                item.product.quantity += item.quantity
                item.product.save()
            purchase.save()
            
            send_mail(
                subject="Purchase Delivered",
                message= f"hi {purchase.supplier.username} delivery has been completed",
                from_email=user.email,
                recipient_list= [purchase.supplier.email],
            )
        
        elif status == "cancelled":
            instance.status = "cancelled"
            purchase.status = "cancelled"
            purchase.save()
            instance.save()
            send_mail(
                subject="Delivery Cancelled",
                message= f"purchase delivery has been cancelled.",
                from_email=user.email,
                recipient_list= [purchase.supplier.email],
                )
            raise serializers.ValidationError("purchase has been cancelled")
        instance.purchase = purchase
        instance.status = status
        instance.delivery = user
        instance.save()
        return instance
  