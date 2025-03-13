from django.shortcuts import render,HttpResponse
from rest_framework import viewsets
from .models import *
from .serializers import *
from .permission import *

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

class DeliveryViewset(viewsets.ModelViewSet):
    
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    # permission_classes = [DeliveryAssigned]
    
    # def get_queryset(self):
    #     user = self.request.user

    #     if user.role == "admin":
    #         return Delivery.objects.all()

    #     return Delivery.objects.filter(delivery=user)

class PurchaseViewset(viewsets.ModelViewSet):
    
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer