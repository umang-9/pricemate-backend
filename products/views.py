from django.shortcuts import render

from rest_framework import generics, permissions, authentication

from .serializers import ProductRequestSerializer


class ProductRequestView(generics.CreateAPIView):
    serializer_class = ProductRequestSerializer
    permission_classes = [permissions.AllowAny, permissions.IsAuthenticated]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
