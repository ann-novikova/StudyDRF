from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from users.models import User


@shared_task
def block_inactive_users():
    """
    Блокирует пользователей, которые не заходили более 30 дней.
    """

    threshold = timezone.now() - timedelta(days=30)

    inactive_users_count = User.objects.filter(
        is_active=True
    ).filter(
        last_login__lt=threshold
    ).exclude(
        is_superuser=True
    ).update(
        is_active=False
    )

    total_blocked = inactive_users_count

    print(f"Successfully blocked {total_blocked} inactive users.")
    return total_blocked