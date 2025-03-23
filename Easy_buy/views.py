from django.shortcuts import render,HttpResponse
from rest_framework import viewsets
from .models import *
from .serializers import *
from .permission import *
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

# Create your views here.
class CategoryViewset(viewsets.ModelViewSet):
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [ViewOnly]
    


class ProductViewset(viewsets.ModelViewSet):
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [ViewOnly] 

class OrderViewset(viewsets.ModelViewSet):
    
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderItemViewset(viewsets.ModelViewSet):
    
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class OrderDeliveryViewset(viewsets.ModelViewSet):
    
    queryset = OrderDelivery.objects.all()
    # permission_classes = [DeliveryAssigned]
    
    # def get_queryset(self):
    #     user = self.request.user

    #     if user.role == "admin":
    #         return Delivery.objects.all()

    #     return Delivery.objects.filter(delivery=user)
    
    def get_serializer_class(self):
        if self.action == "create":
            return OrderDeliveryCreateSerializer
        else:
            return OrderDeliverySerializer

class PurchaseItemViewset(viewsets.ModelViewSet):
    
    queryset = Purchase_Item.objects.all()
    serializer_class = PurchaseItemSerializer

class PurchaseViewset(viewsets.ModelViewSet):
    
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

class PurchaseDeliveryViewset(viewsets.ModelViewSet):
    
    queryset = PurchaseDelivery.objects.all()
    # permission_classes = [DeliveryAssigned]
    
    # def get_queryset(self):
    #     user = self.request.user

    #     if user.role == "admin":
    #         return Delivery.objects.all()

    #     return Delivery.objects.filter(delivery=user)
    
    def get_serializer_class(self):
        if self.action == "create":
            return PurchaseDeliveryCreateSerializer
        # else:
        #     return PurchaseDeliverySerializer

class Dashboard(ViewSet):
    
    def list(self,request):
        # # For Best Customer
        # best_customer = None
        # total = 0  # Highest total spent by a single customer
        # total_revenue = 0  # Total revenue from all customers

        # customers = User.objects.filter(role="customer")
        # for customer in customers:
        #     total_spent = 0  # Total spent by this customer
            
        #     for order in customer.order_set.all():
        #         order_total = 0  # Total for this specific order
                
        #         for item in order.items.all():
        #             price = item.product.price
        #             quantity = item.quantity
        #             order_total += price * quantity
                
        #         total_spent += order_total
        #         total_revenue += order_total  # Add to total revenue
            
        #     if total_spent > total:
        #         total = total_spent
        #         best_customer = customer.username

        # # For Best Supplier
        # best_supplier = None
        # total_quantity = 0  # Highest quantity supplied by a single supplier
        # total_spent_to_suppliers = 0  # Total spent on suppliers

        # suppliers = User.objects.filter(role="supplier")
        # for supplier in suppliers:
        #     total_supplied = 0  # Total quantity supplied by this supplier
        #     supplier_earnings = 0  # Total money this supplier earned

        #     for purchase in supplier.purchase_set.all():
        #         for item in purchase.add_items.all():
        #             price = item.product.price  # Supplier price
        #             quantity = item.quantity
        #             total_supplied += quantity
        #             supplier_earnings += price * quantity
                
        #     total_spent_to_suppliers += supplier_earnings  # Add to total supplier spending

        #     if total_supplied > total_quantity:
        #         total_quantity = total_supplied
        #         best_supplier = supplier.username

        # # Calculate Profit
        # profit = total_revenue - total_spent_to_suppliers
        
        best_spent = 0
        best_customer = None
        total_sold = 0
        total_ordered = 0
        best_supplier = None
        best_supplied = 0
        customers = User.objects.filter(role = "customer")
        suppliers = User.objects.filter(role = "supplier")
        
        for customer in customers:
            total_spent = 0 
            for orders in customer.order_set.all():
                if orders.status == "completed":
                    order_total = 0
                    for order_items in orders.items.all():
                        price = order_items.product.price
                        quantity = order_items.quantity
                        order_total += price * quantity
                    total_spent += order_total
                    total_sold += order_total
            
            if total_spent > best_spent:
                best_spent = total_spent
                best_customer = customer.username      
        
        for supplier in suppliers:
            total_supplied = 0
            for purchase in supplier.purchase_set.all():
                if purchase.status == "completed":
                    for purchase_item in purchase.add_items.all():
                        
                        price = purchase_item.product.price
                        quantity = purchase_item.quantity
                        supply_total = price * quantity
                    total_supplied += supply_total
                    total_ordered += supply_total
            
            if total_supplied > best_supplied:
                best_supplied = total_supplied
                best_supplier = supplier.username
        
            profit = total_sold - total_ordered
        
        stats = {
            "total_users": User.objects.count(),
            "customers": User.objects.filter(role = "customer").count(),
            "suppliers": User.objects.filter(role = "supplier").count(),
            "deliverers": User.objects.filter(role = "delivery").count(),
            "admins":User.objects.filter(role = "admin").count(),
            "best_customer":best_customer,
            "total_spent_by_best_customer":total_spent,
            "best_supplier":best_supplier,
            "total_supplied_by_best_supplier":total_supplied,
            "total_ordered":total_ordered,
            "total_revenue": total_sold,
            "profit/loss": profit,
            "orders_pending":Order.objects.filter(status = "pending").count(),
            "orders_completed":Order.objects.filter(status = "completed").count(),
        }
        return Response(stats)