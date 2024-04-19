from .serializers import SubscriberSerializer
from .models import Subscriber

from django.shortcuts import render

from rest_framework import generics, permissions, authentication


class SubscriberCreateView(generics.CreateAPIView):
    serializer_class = SubscriberSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def perform_create(self, serializer):
        email = serializer.validated_data.get("email")
        queryset = Subscriber.objects.filter(email=email)
        if queryset.exists():
            object = queryset.first()
            object.is_active = True
            object.save()
        else:
            # is_active is forcefully True on CreateView
            serializer.save(is_active=True)
