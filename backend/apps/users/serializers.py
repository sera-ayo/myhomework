from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, trim_whitespace=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "is_staff", "date_joined"]
