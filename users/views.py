from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from study.models import Course
from users.models import Payment, Subscription, User
from users.permissions import UserIsOwner
from users.serializers import (PaymentSerializer, PublicUserSerializer,
                               UserSerializer)


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
    permission_classes = (IsAuthenticated,)
    serializer_class = PublicUserSerializer


class UserRetriveApiView(RetrieveAPIView):
    """Контроллер для просмотра данных о пользователе"""

    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        obj = self.get_object()

        if self.request.user == obj:
            return UserSerializer

        return PublicUserSerializer


class UserUpdateApiView(UpdateAPIView):
    """Контроллер для редактирования данных пользователя"""

    queryset = User.objects.all()
    permission_classes = (
        UserIsOwner,
        IsAuthenticated,
    )
    serializer_class = UserSerializer


class UserDestroyApiView(DestroyAPIView):
    """Контроллер для удаления данных пользователя"""

    queryset = User.objects.all()
    permission_classes = (
        UserIsOwner,
        IsAuthenticated,
    )
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


class SubscriptionAPIView(APIView):
    """Контроллер для создания подписки"""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Метод для создания и удаления подписки"""

        user = request.user
        course_id = request.data.get("course_id")
        if not course_id:
            return Response(
                {"detail": "Необходимо указать 'course_id'."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        course_item = get_object_or_404(Course, pk=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка успешно удалена"
            response_status = status.HTTP_200_OK
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка успешно добавлена"
            response_status = status.HTTP_201_CREATED
        return Response({"message": message}, status=response_status)
