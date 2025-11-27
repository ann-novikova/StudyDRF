from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (PaymentCreateAPIView, PaymentListAPIView,
                         PaymentRetrievePIView, SubscriptionAPIView,
                         UserCreateApiView, UserDestroyApiView,
                         UserListApiView, UserRetriveApiView,
                         UserUpdateApiView)

app_name = UsersConfig.name

router = SimpleRouter()

urlpatterns = [
    path("users/", UserListApiView.as_view(), name="users"),
    path("users/<int:pk>/", UserRetriveApiView.as_view(), name="user_retrieve"),
    path("users/<int:pk>/update/", UserUpdateApiView.as_view(), name="user_update"),
    path("users/<int:pk>/delete/", UserDestroyApiView.as_view(), name="user_delete"),
    path("users/payments/", PaymentListAPIView.as_view(), name="payments"),
    path(
        "users/payments/proceed/", PaymentCreateAPIView.as_view(), name="create_payment"
    ),
    path(
        "users/payments/<int:pk>/",
        PaymentRetrievePIView.as_view(),
        name="payment_details",
    ),
    path("register/", UserCreateApiView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path(
        "subscriptions/activate/",
        SubscriptionAPIView.as_view(),
        name="subscription_activate",
    ),
]

urlpatterns += router.urls
