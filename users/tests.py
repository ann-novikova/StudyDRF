from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from study.models import Course
from users.models import Subscription, User


class SubscriptionTestCase(APITestCase):
    """ "Класс для тестирования подписки"""

    def setUp(self):
        self.user = User.objects.create(email="test@sky.pro")
        self.course = Course.objects.create(name="Test_course", description="Desc")
        self.url = reverse("users:subscription_activate")
        self.client.force_authenticate(user=self.user)

    def test_subscribe_creates_subscription(self):
        """Тестирование создания подписки"""
        response = self.client.post(self.url, {"course_id": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"message": "Подписка успешно добавлена"})
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_subscribe_deletes_subscription(self):
        """Тестирование удаления подписки"""
        Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post(self.url, {"course_id": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "Подписка успешно удалена"})
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_missing_course_id_returns_400(self):
        """Тестирование подписки на пустой курс"""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {"detail": "Необходимо указать 'course_id'."})

    def test_invalid_course_id_returns_404(self):
        """Тестирование подписки на несуществующий курс"""
        response = self.client.post(self.url, {"course_id": 999999}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthenticated_returns_401(self):
        """Тестирование подписки для неавторизованного пользователя"""
        anonym = APIClient()
        response = anonym.post(self.url, {"course_id": self.course.pk}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
