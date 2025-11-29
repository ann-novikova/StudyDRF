from celery import shared_task
from django.core.mail import send_mail

from config.settings import DEFAULT_FROM_EMAIL
from study.models import Course
from users.models import Subscription


@shared_task()
def send_course_update_email(course_id):
    """
    Асинхронно отправляет письмо всем подписчикам конкретного курса.
    Аргумент: course_id (int)
    Возвращает количество отправленных сообщений.
    """
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return 0

    subscriptions = Subscription.objects.filter(course=course)
    emails = []
    for s in subscriptions:
        emails.append(s.user.email)

    subject = f"Обновление курса: {course.name}"
    message = "Посмотрите последние обновления курса!"
    print("emails")
    if emails:
        send_mail(subject, message, DEFAULT_FROM_EMAIL, emails)
        print(f"Sent update email for course {course_id} to {len(emails)} users.")
        return len(emails)
    return 0
