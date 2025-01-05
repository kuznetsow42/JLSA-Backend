from rest_framework import serializers
from .models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "avatar", "streak")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "avatar", "streak", "email")
        extra_kwargs = {
            "password": {"write_only": True},
            "streak": {"read_only": True},
        }

