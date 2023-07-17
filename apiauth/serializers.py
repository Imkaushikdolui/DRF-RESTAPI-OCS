from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Account
from api.models import *


# class AccountSerializer(serializers.ModelSerializer):
#     # password = serializers.CharField(
#     #     write_only=True, style={'input_type': 'password'})

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'pk',
            'role',
            'name',
            'username',
            'email',
            'password',
            'is_verified'
        ]
        extra_kwargs = {'password': {'write_only': True}}  # Hide password during retrieval

    def create(self, validated_data):
        role = validated_data.get('role')
        password = validated_data.pop('password')
        account = Account.objects.create_user(password=password, **validated_data)

        if role == 'teacher':
            Teacher.objects.create(name=validated_data['name'], teacher_id=account)

        if role == 'student':
            Student.objects.create(name=validated_data['name'], student_id=account)

        return account
    
class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
class AccountDetailSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%S%z")
    last_login = serializers.DateTimeField(read_only=True, format="%Y-%m-%dT%H:%M:%S%z")
    is_admin = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = Account
        fields = [
            'role',
            'name',
            'username',
            'email',
            'is_verified',
            'date_joined',
            'last_login',
            'is_admin',
            'is_active',
            'is_staff',
            'is_superuser',
        ]

