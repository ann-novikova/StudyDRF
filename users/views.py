from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
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


class UserRetriveApiView(RetrieveAPIView):
    """Контроллер для просмотра данных о пользователе"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateApiView(UpdateAPIView):
    """Контроллер для редактирования данных пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDestroyApiView(DestroyAPIView):
    """Контроллер для удаления данных пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateApiView(CreateAPIView):
    """Контроллер для создания пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Метод для создания пользователя"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

