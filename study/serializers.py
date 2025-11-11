from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from study.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    """ "Сериализатор для урока"""

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    """
    Сериализатор для модели Курса (Course).

    Выводит:
    основную информацию о курсе,
    список всех уроков курса (вложенные данные),
    общее количество уроков в курсе.
    """

    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        """Возвращает количество уроков, связанных с курсом."""
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = ["name", "description", "preview", "lessons_count", "lessons"]
