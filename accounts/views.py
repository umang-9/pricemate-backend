from .serializers import UserSerializer

from rest_framework import generics, permissions

from django.contrib.auth.models import User


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
