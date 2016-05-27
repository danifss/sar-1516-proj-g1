from rest_framework import serializers
from .models import User, Services, PSW


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services


class PSWSerializer(serializers.ModelSerializer):
    class Meta:
        model = PSW
