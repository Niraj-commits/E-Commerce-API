
from rest_framework import serializers
from .models import *

class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ['id','username','password','address','email','phone']
    
    def create(self,validated_data):
        validated_data['role'] = 'customer' #setting role to customer

        user = User.objects.create_user(**validated_data) #create_user is to handle hashing automatically
        return user

class SupplierSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ['id','username','password','address','email','phone','company_name']
    
    def create(self,validated_data):
        validated_data['role'] = 'supplier'
        user = User.objects.create_user(**validated_data)
        return user

class DeliverySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    
    class Meta:
        model = User
        fields = ['id','username','password','address','email','vehicle_type','availability_status' ]
    def create(self,validated_data):
        validated_data['role'] = 'delivery'
        user = User.objects.create_user(**validated_data)
        return user