from django.contrib.auth.models import AbstractUser
from django.db import models

from study.models import Course, Lesson


class User(AbstractUser):
    """Кастомная модель пользователя"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(
        max_length=50, verbose_name="Имя", blank=True, null=True
    )
    last_name = models.CharField(
        max_length=100, verbose_name="Фамилия", blank=True, null=True
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите свой аватар",
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=100,
        verbose_name="Город",
        help_text="Введите город проживания",
        blank=True,
        null=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """Возвращает строковое представление объекта User"""
        return self.email or f"User #{self.pk}"


class Payment(models.Model):
    """
    Модель для хранения информации об оплатах пользователей за курсы или уроки.

    Платеж может быть связан либо с конкретным уроком, либо с курсом.
    Поддерживает два типа оплаты: наличные и безналичный перевод.

    user (ForeignKey): Ссылка на пользователя, совершившего оплату.
    date_pay (DateField): Дата совершения оплаты. Автоматически устанавливается при создании.
    paid_lesson (ForeignKey): Ссылка на урок, за который произведена оплата. Необязательное поле.
    paid_course (ForeignKey): Ссылка на курс, за который произведена оплата. Необязательное поле.
    payment_amount (PositiveIntegerField): Сумма оплаты в рублях (или другой валюте). По умолчанию 0.
    type_pay (CharField): Тип оплаты — наличные или безналичный расчёт.
     Выбор ограничен константами TYPE_CASH и TYPE_TRANSFER_ACCOUNT.
    """

    TYPE_CASH = "cash"
    TYPE_TRANSFER_ACCOUNT = "non_cash"

    STATUS_CHOICES = [
        (TYPE_CASH, "Наличные"),
        (TYPE_TRANSFER_ACCOUNT, "Перевод на счет"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payments",
    )

    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Оплченный курс",
        related_name="paid_courses",
    )

    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        related_name="paid_lesson",
    )

    date_pay = models.DateTimeField(auto_now=True, verbose_name="Дата оплаты")

    payment_amount = models.PositiveIntegerField(default=0, verbose_name="Сумма оплаты")

    type_pay = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        verbose_name="Вид оплаты",
    )

    class Meta:
        """
        Определяет человекочитаемое имя модели и его множественную форму
        для отображения в интерфейсе администратора.
        """

        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        """Возвращает строковое представление объекта Pay."""
        return f"Платеж от {self.user.email} на сумму {self.payment_amount} руб."
