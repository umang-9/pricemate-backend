from rest_framework import serializers
from .models import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = Subscriber
        fields = ["email", "is_active"]
