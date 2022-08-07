from PIL import Image
from django.db import transaction
from rest_framework import serializers

from clients.models import User
from clients.watermark import add_watermark


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'gender',
            'avatar',
        )


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'gender',
            'avatar',
        )

    @transaction.atomic()
    def create(self, validated_data):
        user = super().create(validated_data)   # type: User
        if user.avatar:
            img = Image.open(user.avatar)
            watermark = Image.open("clients/static/clients/img/watermark.png")
            result = add_watermark(img, watermark)
            result.save(user.avatar.path)
        return user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'gender',
            'avatar',
        )
