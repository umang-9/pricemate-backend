from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        label="Password",
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ("email", "password", "first_name", "last_name")

    def validate_email(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Email already exists!")
        return value

    def create(self, validated_data):
        validated_data["username"] = validated_data.get("email")
        # user = super(UserSerializer, self).create(validated_data)
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email", write_only=True)
    password = serializers.CharField(
        label="Password",
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label="Token", read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            if not user:
                msg = "Unable to log in with provided credentials."
                # raise serializers.ValidationError(msg, code="authorization")
                raise serializers.ValidationError("Invalid username or password!")
        else:
            msg = 'Must include "email" and "password".'
            # raise serializers.ValidationError(msg, code="authorization")
            raise serializers.ValidationError("Email and Password are required!")

        attrs["user"] = user
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
