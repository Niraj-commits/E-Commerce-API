from rest_framework import serializers
from .models import *


class AdminSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone', 'address']

    def create(self, validated_data):
        validated_data['role'] = 'admin'
        user = User.objects.create_user(**validated_data)
        return user
    
class CustomerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone', 'address']

    def create(self, validated_data):
        validated_data['role'] = 'customer'
        user = User.objects.create_user(**validated_data)
        return user

class SupplierSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone', 'address', 'company_name']

    def create(self, validated_data):
        validated_data['role'] = 'supplier'
        user = User.objects.create_user(**validated_data)
        return user

class DeliverySerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'phone', 'address','license_no','vehicle_type']

    def create(self, validated_data):
        validated_data['role'] = 'delivery'
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
