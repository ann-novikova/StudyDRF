import logging
from datetime import timedelta

from django.utils import timezone
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from study.models import Course, Lesson
from study.paginations import CustomPagination
from study.serializers import CourseSerializer, LessonSerializer
from study.tasks import send_course_update_email
from users.permissions import IsModer, IsOwner

logger = logging.getLogger(__name__)


class CourseViewSet(ModelViewSet):
    """Контроллер для курсов"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        logger.info("perform_update called for %s", self.get_object().pk)
        course = serializer.save()
        logger.info(
            "After save: last_notified_at=%r, updated_at=%r",
            course.last_notified_at,
            course.updated_at,
        )

        now = timezone.now()
        time_for_update = timedelta(minutes=1)

        if course.last_notified_at is None:
            logger.info("Condition passed, sending task for course %s", course.pk)
            send_course_update_email.delay(course.pk)
        elif (
            now - course.last_notified_at
        ) >= time_for_update and course.updated_at > course.last_notified_at:
            logger.info("Condition passed, sending task for course %s", course.pk)
            send_course_update_email.delay(course.pk)
        else:
            logger.info("Condition not passed, skipping sending")


class LessonCreateApiView(CreateAPIView):
    """Контроллер для создания урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        ~IsModer,
        IsAuthenticated,
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListApiView(ListAPIView):
    """Контроллер для просмотра списка уроков"""

    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetriveApiView(RetrieveAPIView):
    """Контроллер для просмотра урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )


class LessonUpdateApiView(UpdateAPIView):
    """Контроллер для редактирования урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsModer | IsOwner,
    )


class LessonDestroyApiView(DestroyAPIView):
    """Контроллер для удаления урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )
