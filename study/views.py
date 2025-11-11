from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from study.models import Course, Lesson
from study.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer


class CourseViewSet(ModelViewSet):
    """Контроллер для курсов"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer,)
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    """Контроллер для создания урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated,)


class LessonListApiView(ListAPIView):
    """Контроллер для просмотра списка уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetriveApiView(RetrieveAPIView):
    """Контроллер для просмотра урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateApiView(UpdateAPIView):
    """Контроллер для редактирования урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyApiView(DestroyAPIView):
    """Контроллер для удаления урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated,)
