from django.contrib import admin
from django.urls import path, include

from accounts.views import UserCreateAPIView, LoginAPIView, PasswordResetView

from products.views import (
    # product
    ProductCreateView,
    ProductDetailView,
    ProductListView,
    # product request
    ProductRequestCreateView,
    ProductRequestDeleteView,
    ProductRequestListView,
    # price
    PriceCreateView,
    # Watch
    WatchCreateView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # auth
    path("login/", LoginAPIView.as_view()),
    path("signup/", UserCreateAPIView.as_view()),
    path("reset-password/", PasswordResetView().as_view()),
    path(
        "forgot-password/",
        include("django_rest_passwordreset.urls", namespace="forgot_password"),
    ),
    # product request
    path("products/request/delete/<int:pk>/", ProductRequestDeleteView().as_view()),
    path("products/request/list/", ProductRequestListView().as_view()),
    path("products/request/", ProductRequestCreateView().as_view()),
    # price
    path("products/price/", PriceCreateView().as_view()),
    # product
    path("products/detail/<int:pk>/", ProductDetailView().as_view()),
    path("products/list/", ProductListView().as_view()),
    path("products/", ProductCreateView().as_view()),
    # watch
    path("products/watch/", WatchCreateView().as_view()),
]
