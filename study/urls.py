from django.urls import path
from rest_framework.routers import SimpleRouter

from study.apps import StudyConfig
from study.views import (
    CourseViewSet,
    LessonCreateApiView,
    LessonDestroyApiView,
    LessonListApiView,
    LessonRetriveApiView,
    LessonUpdateApiView,
)

app_name = StudyConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lessons_list"),
    path("lessons/<int:pk>/", LessonRetriveApiView.as_view(), name="lessons_retrieve"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lessons_create"),
    path(
        "lessons/<int:pk>/delete/",
        LessonDestroyApiView.as_view(),
        name="lessons_delete",
    ),
    path(
        "lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lessons_update"
    ),
]

urlpatterns += router.urls
