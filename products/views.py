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
        queryset = Product.objects.all()

        # adding watch details into the queryset
        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.prefetch_related(
                Prefetch("watch_set", queryset=Watch.objects.filter(user=user))
            )
        else:
            queryset = queryset.prefetch_related(
                Prefetch("watch_set", queryset=Watch.objects.filter(user=None))
            )

        # adding price details into the queryset
        queryset = queryset.prefetch_related(
            Prefetch("price_set", queryset=Price.objects.all())
        )

        # ordering
        order_by = self.request.query_params.get("orderby", "-updated")
        if order_by not in [
            "updated",
            "-updated",
            "timestamp",
            "-timestamp",
            "title",
            "-title",
            "price__amount",
            "-price__amount",
        ]:
            order_by = "-updated"
        # order_by = "-price__amount"  # TODO: remove this line
        queryset = queryset.order_by(order_by)
        # queryset = queryset.distinct("id") # only works for postgresql

        # filtering
        filter_by = self.request.query_params.get("filterby", None)

        if filter_by == "watching":
            if user.is_authenticated:
                queryset = queryset.filter(watch__user=user)
            else:
                return queryset.none()

        if filter_by is not None and filter_by.startswith("price__"):
            if len(filter_by.split("__")) != 3:
                return queryset.none()
            _, price_start, price_end = filter_by.split("__")
            queryset = queryset.filter(
                price__amount__gt=price_start, price__amount__lt=price_end
            )
        return queryset


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
            object = serializer.save()
            object.product.save()
        else:
            prices[0].product.save()

            last_price = prices.order_by("-timestamp")[0].amount

            if amount != last_price:
                object = serializer.save()


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

    def get_queryset(self):
        return Watch.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        user = self.request.user
        if instance.user == user:
            instance.delete()


# OJ4OhUIOOqlMXudn
