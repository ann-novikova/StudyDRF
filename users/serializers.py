from rest_framework import serializers
from rest_framework.relations import StringRelatedField

from users.models import Payment, Subscription, User


class PaymentSerializer(serializers.ModelSerializer):
    """ "Сериализатор для платежей"""

    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    """ "Сериализатор для подписки"""

    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Subscription
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """ "Сериализатор для пользователя"""

    payments = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone", "city", "payments"]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        """Метод для обновления пароля пользователя"""
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)

        return super().update(instance, validated_data)


class PublicUserSerializer(serializers.ModelSerializer):
    """ "Сериализатор для пользователя при публичном просмотре"""

    subscriptions = SubscriptionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "avatar", "city", "subscriptions"]
