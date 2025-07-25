from rest_framework import serializers

from goroskop.apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "language",
            "zodiac_sign",
            "telegram_id",
            "telegram_username",
            "first_name",
            "last_name",
        ]

    def create(self, validated_data):
        print(1)
        ModelClass = self.Meta.model
        instance = ModelClass._default_manager.update_or_create(**validated_data)
        return instance
