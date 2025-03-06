from django.shortcuts import render
from rest_framework import generics
from .serializers import *

# Create your views here.
class CustomerRegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSerializer
    
class CustomerRegisterUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = CustomerSerializer

class SupplierRegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = SupplierSerializer

class DeliveryRegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = DeliverySerializer