from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    """ "Сериализатор для платежей"""

    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    """ "Сериализатор для пользователя"""

    payments = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone", "city", "payments"]
        read_only_fields = ["id", "email"]

    def update(self, instance, validated_data):
        """Метод для обновления пароля пользователя"""
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)

        return super().update(instance, validated_data)


class PublicUserSerializer(ModelSerializer):
    """ "Сериализатор для пользователя при публичном просмотре"""

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "avatar", "city"]
