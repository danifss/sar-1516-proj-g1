from rest_framework import serializers
from core.models import User, Service


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service


# class BrokerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Broker
