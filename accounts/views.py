from .serializers import UserSerializer, LoginSerializer

from rest_framework import generics, permissions, views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django.contrib.auth.models import User


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class LoginAPIView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
