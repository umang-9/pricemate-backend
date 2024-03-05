from .serializers import UserSerializer, LoginSerializer, PasswordResetSerializer

from rest_framework import generics, permissions, views, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.core.mail import send_mail


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


class PasswordResetView(generics.UpdateAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # check old password
            old_password = serializer.validated_data.get("old_password")
            if not request.user.check_password(old_password):
                return Response(
                    {"detail": "Invalid password!"}, status=status.HTTP_400_BAD_REQUEST
                )

            # old password is correct
            new_password = serializer.validated_data.get("new_password")
            request.user.set_password(new_password)
            request.user.save()

            # send email notification
            send_mail(
                "Attention! Password reset!",
                """
Dear user,
Your password is successfully updated!
If it wasn't you, please reach out to customer service!

Thank you.
                """,
                "from@example.com",
                [request.user.email],
                fail_silently=False,
            )

            return Response({"detail": "Password updated!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
