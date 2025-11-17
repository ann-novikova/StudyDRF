from rest_framework import serializers

from study.models import Course, Lesson
from study.validators import validate_url
from users.models import Subscription


class LessonSerializer(serializers.ModelSerializer):
    """ "Сериализатор для урока"""

    url = serializers.CharField(validators=[validate_url])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Курса (Course).

    Выводит:
    основную информацию о курсе,
    список всех уроков курса (вложенные данные),
    общее количество уроков в курсе.
    """

    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        """Возвращает количество уроков, связанных с курсом."""
        return Lesson.objects.filter(course=obj).count()

    def get_is_subscribed(self, obj):
        """Возвращает булево значение для подписки"""
        request = self.context.get("request")
        if not request or request.user.is_anonymous:
            return False
        user = request.user
        return Subscription.objects.filter(user=user, course=obj).exists()

    class Meta:
        model = Course
        fields = [
            "id",
            "name",
            "description",
            "preview",
            "lessons_count",
            "lessons",
            "is_subscribed",
        ]
        read_only_fields = ["id"]
