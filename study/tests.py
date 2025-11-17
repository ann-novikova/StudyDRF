from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from study.models import Course, Lesson
from users.models import Subscription, User


class LessonTestCase(APITestCase):
    """Класс для тестрования CRUD урока"""

    def setUp(self):
        self.user = User.objects.create(email="test@sky.pro")
        self.course = Course.objects.create(name="Python test", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Unittest", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        """Тестирование получения деталей урока"""
        url = reverse("study:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        """Тестирование создание урока"""
        url = reverse("study:lessons_create")
        data = {"name": "Pytest", "url": "http://youtube.com/lesson1/"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_validate_url(self):
        """Тестирование создания урока с невалидной ссылкой"""
        url = reverse("study:lessons_create")
        data = {"name": "Pytest", "url": "http://myaccount.com/lesson1/"}
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data.get("url"), ["Допускаются только ссылки на youtube.com"])

    def test_update_lesson(self):
        """Тестирование побновления деталей урока"""
        url = reverse("study:lessons_update", args=(self.lesson.pk,))
        data = {"url": "http://youtube.com/lesson1/"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("url"), "http://youtube.com/lesson1/")

    def test_destroy_lesson(self):
        """Тестирование удаления урока"""
        url = reverse("study:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lessons_list(self):
        """Тестирование вывода списка уроков"""
        url = reverse("study:lessons_list")
        response = self.client.get(url)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "url": None,
                    "name": "Unittest",
                    "description": None,
                    "preview": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), result)


class CourseTestCase(APITestCase):
    """Класс для тестрования CRUD курса"""

    def setUp(self):
        self.user = User.objects.create(email="test@sky.pro")
        self.course = Course.objects.create(name="Python test", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Unittest", course=self.course, owner=self.user
        )
        self.subsription = Subscription.objects.create(
            course=self.course, user=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        """Тестирование вывода деталей курса"""
        url = reverse("study:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.course.name)

    def test_course_create(self):
        """Тестирование для создания курса"""
        url = reverse("study:course-list")
        data = {"name": "Java-разработчик"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        """Тестирование обновления деталей курса"""
        url = reverse("study:course-detail", args=(self.course.pk,))
        data = {"name": "Java-разработчик"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Java-разработчик")

    def test_course_delete(self):
        """Тестирование удаления курса"""
        url = reverse("study:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        """Тестирование вывода списка курсов"""
        url = reverse("study:course-list")
        response = self.client.get(url)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "name": self.course.name,
                    "description": self.course.description,
                    "preview": None,
                    "lessons_count": 1,
                    "lessons": [
                        {
                            "id": self.lesson.pk,
                            "url": self.lesson.url,
                            "name": self.lesson.name,
                            "description": self.lesson.description,
                            "preview": None,
                            "course": self.course.pk,
                            "owner": self.user.pk,
                        }
                    ],
                    "is_subscribed": True,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), result)
