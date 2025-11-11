from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class PaymentViewSet(ReadOnlyModelViewSet):
    """Контроллер для вывода списка платежей с фильтрацией и сортировкой по дате"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    search_fields = ["paid_course__name", "paid_lesson__name", "type_pay"]
    ordering_fields = ["date_pay"]


class UserListApiView(ListAPIView):
    """Контроллер для вывода пользователей с историей платежей"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
