from django.shortcuts import render
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