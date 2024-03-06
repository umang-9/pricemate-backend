from django.contrib import admin
from django.urls import path, include

from accounts.views import UserCreateAPIView, LoginAPIView, PasswordResetView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("login/", LoginAPIView.as_view()),
    path("signup/", UserCreateAPIView.as_view()),
    path("reset-password/", PasswordResetView().as_view()),
    path(
        "forgot-password/",
        include("django_rest_passwordreset.urls", namespace="forgot_password"),
    ),
]
