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

from django.core.mail import send_mail
def sendmail(request):
    send_mail(
        subject = "Order",
        message = "Your order has been delivered.",
        from_email = 'karki.ni018@gmail.com',
        recipient_list = ['abc@gmail.com'],
    )
    return HttpResponse({"details":"mail is sent"})