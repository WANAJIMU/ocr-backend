from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=255, required=True)
#     password = serializers.CharField(max_length=128, write_only=True, required=True)


class LoginSerializer(serializers.Serializer):
    identity = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(max_length=128, write_only=True, required=True)
