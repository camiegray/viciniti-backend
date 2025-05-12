from rest_framework import serializers
from .models import User, Service, Appointment, DiscountRule
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'role', 'location']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class ServiceSerializer(serializers.ModelSerializer):
    provider = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Service
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(read_only=True)
    service_title = serializers.ReadOnlyField(source='service.title')
    service_details = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['id', 'customer', 'service', 'service_title', 'service_details', 'datetime', 'location', 'discounted_price']

    def get_service_details(self, obj):
        return {
            'title': obj.service.title,
            'description': obj.service.description,
            'base_price': obj.service.base_price,
            'duration_minutes': obj.service.duration_minutes
        }


class DiscountRuleSerializer(serializers.ModelSerializer):
    provider = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DiscountRule
        fields = '__all__'
