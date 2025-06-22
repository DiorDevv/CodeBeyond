from django.contrib.auth import authenticate
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import CustomUser


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'password', 'is_staff', 'is_active')


class UserSerializer(BaseUserSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = CustomUser
        fields = ('id', 'email', 'username', 'password', 'is_staff', 'is_active')



class EmailSerializers(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError('Passwords do not match')
        attrs.pop('confirm_password')
        return super().validate(attrs)


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError('Passwords do not match')
        return super().validate(attrs)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()
