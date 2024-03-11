from django.db.models import Q

from rest_framework import serializers

from .models import ProductRequest


class ProductRequestSerializer(serializers.ModelSerializer):
    def validate_link(self, link):
        if (not "amazon.ca" in link) and (not "a.co/d/" in link):
            raise serializers.ValidationError("Link not supported!")
        link = link.split("?")[0]

        if ProductRequest.objects.filter(Q(link=link) | Q(short_link=link)).exists():
            raise serializers.ValidationError("Link already exists!")

        _link = link.split("https://")

        # validating amazon.ca links
        if "amazon.ca" in link:
            if _link.split("/")[2] != "dp":
                raise serializers.ValidationError("Link not supported!")

        # validating a.co links
        if "a.co/d/" in link:
            if _link.split("/")[1] != "d":
                raise serializers.ValidationError("Link not supported!")

        return link

    class Meta:
        model = ProductRequest
        fields = ["id", "link", "user"]
