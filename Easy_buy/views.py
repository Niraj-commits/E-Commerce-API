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
        
        best_customer = None
        total = 0
        customers = User.objects.filter(role = "customer")
        for customer in customers:
            total_spent = 0
            
            for order in customer.order_set.all():
                for item in order.items.all():
                    price = item.product.price
                    quantity = item.quantity
                    total_spent += price * quantity
            
            if total_spent > total:
                total = total_spent
                best_customer = customer.username
        
        stats = {
            "total_users": User.objects.count(),
            "customers": User.objects.filter(role = "customer").count(),
            "suppliers": User.objects.filter(role = "supplier").count(),
            "deliverers": User.objects.filter(role = "delivery").count(),
            "admins":User.objects.filter(role = "admin").count(),
            "best_customer":best_customer,
            "spent_by_best_customer":total,
        }
        return Response(stats)