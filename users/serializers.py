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
        fields = ["email", "password", "phone", "city", "payments"]
