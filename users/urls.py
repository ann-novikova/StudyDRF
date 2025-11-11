from django.urls import path
from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import PaymentViewSet, UserListApiView

app_name = UsersConfig.name

router = SimpleRouter()
router.register("payments", PaymentViewSet)

urlpatterns = [
    path("users/", UserListApiView.as_view(), name="users"),
]

urlpatterns += router.urls
