from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from django.conf import settings
from .models import Course
from users.models import Subscription


def mark_course_for_notification(course_id, hours=4):
    """
    Функиия для получения курса, который обновлен если
    он не обновлялся более `hours`. Возвращает True если пометили (и значит
    нужно отправлять письмо).
    """
    now = timezone.now()
    threshold = now - timedelta(hours=hours)
    if Course.objects.filter(
        id=course_id,
        updated_at__lt=threshold
    ):
        return True
    return False
