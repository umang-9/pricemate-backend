from django.db.models import Prefetch

from rest_framework import generics, permissions, authentication, pagination

from .models import ProductRequest, Product, Price, Watch

from .serializers import (
    PriceSerializer,
    ProductRequestSerializer,
    ProductSerializer,
    WatchSerializer,
)


class ProductRequestCreateView(generics.CreateAPIView):
    serializer_class = ProductRequestSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class ProductRequestListView(generics.ListAPIView):
    queryset = ProductRequest.objects.all()
    serializer_class = ProductRequestSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]
    pagination_class = pagination.PageNumberPagination
    page_size = 10


class ProductRequestDeleteView(generics.DestroyAPIView):
    queryset = ProductRequest.objects.all()
    serializer_class = ProductRequestSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Product.objects.all().prefetch_related(
                Prefetch("watch_set", queryset=Watch.objects.filter(user=user))
            )
        else:
            return Product.objects.all().prefetch_related(
                Prefetch("watch_set", queryset=Watch.objects.filter(user=None))
            )


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def get_queryset(self):
        qs = Product.objects.all()
        return qs


class PriceCreateView(generics.CreateAPIView):
    serializer_class = PriceSerializer
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def perform_create(self, serializer):
        product = serializer.validated_data.get("product")
        amount = serializer.validated_data.get("amount")

        prices = Price.objects.filter(product=product)
        if not prices.exists():
            return super().perform_create(serializer)

        last_price = prices.order_by("-timestamp")[0].amount

        if amount != last_price:
            return super().perform_create(serializer)


class WatchCreateView(generics.CreateAPIView):
    serializer_class = WatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class WatchDeleteView(generics.DestroyAPIView):
    queryset = Watch.objects.all()
    serializer_class = WatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [
        authentication.TokenAuthentication,
        authentication.SessionAuthentication,
    ]

    def perform_destroy(self, instance):
        user = self.request.user
        if instance.user == user:
            instance.delete()
