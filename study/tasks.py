from celery import shared_task
from django.core.mail import send_mail

from config.settings import DEFAULT_FROM_EMAIL
from .models import Course
from users.models import Subscription
from .services import mark_course_for_notification


@shared_task()
def send_course_update_email(self, course_id):
    """
    Асинхронно отправляет письмо всем подписчикам конкретного курса.
    Аргумент: course_id (int)
    Возвращает количество отправленных сообщений.
    """
    updated = mark_course_for_notification(course_id)
    if not updated:
        return 0
    course = Course.objects.get(pk=course_id)
    if not course:
        return 0

    subscriptions = Subscription.objects.filter(course=course)
    emails = []
    for s in subscriptions:
        emails.append(s.user.email)
    subject = f"Обновление курса: {course.name}"
    message = "Посмотрите последние обновления курса!"
    if emails:
        send_mail(
            subject,
            message,
            DEFAULT_FROM_EMAIL,
            emails
        )

