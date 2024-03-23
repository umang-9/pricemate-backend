from django.db.models import Q

from rest_framework import serializers

from .models import ProductRequest, Product, Price, Watch


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ["id", "amount", "product", "timestamp"]


class WatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watch
        fields = ["id", "product"]  # "users" not needed (get it through request object)

    def validate(self, attrs):
        request = self.context.get("request")
        product = attrs.get("product")

        # already watching
        if Watch.objects.filter(user=request.user, product=product).exists():
            raise serializers.ValidationError("Already watching this product!")

        return super().validate(attrs)


class ProductSerializer(serializers.ModelSerializer):
    prices = PriceSerializer(many=True, source="price_set", read_only=True)
    # watch = WatchSerializer(many=True, source="watch_set", read_only=True)
    watch = serializers.SerializerMethodField()

    def get_watch(self, obj):
        request = self.context.get("request")
        if request.user.is_authenticated:
            qs = obj.watch_set.filter(user=request.user)
            return WatchSerializer(qs, many=True).data
        else:
            return None

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "image",
            "link",
            "platform",
            "about",
            "prices",
            "watch",
        ]


class ProductRequestSerializer(serializers.ModelSerializer):
    def validate_link(self, link):
        if not "amazon.ca" in link:
            raise serializers.ValidationError("Link not supported!")

        link_to_save = link.split("?")[0]
        link_to_save = link_to_save.split("https://")[1]

        # validating amazon.ca links
        # if link_to_save.split("/")[2] != "dp":
        # raise serializers.ValidationError("Link not supported!")

        link_parts = link_to_save.split("/")
        link_to_save = "https://"
        previous_part = ""
        for part in link_parts:
            if previous_part == "dp":
                link_to_save += part + "/"
                break
            link_to_save += part + "/"
            previous_part = part

        # link_to_save = "https://" + "/".join(link_to_save.split("/")[0:4])

        if (
            Product.objects.filter(link=link_to_save).exists()
            or ProductRequest.objects.filter(link=link_to_save).exists()
        ):
            raise serializers.ValidationError("Link already exists!")

        return link_to_save

    class Meta:
        model = ProductRequest
        fields = ["id", "link", "user"]
