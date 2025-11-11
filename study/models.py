from django.db import models


class Course(models.Model):
    """Класс для курса"""

    name = models.CharField(max_length=150, verbose_name="Наименование курса")
    preview = models.ImageField(
        upload_to="study/courses/",
        verbose_name="Превью",
        blank=True,
        null=True,
        help_text="Превью курса",
    )
    description = models.TextField(
        max_length=300, verbose_name="Описание курса", blank=True, null=True
    )

    def __str__(self):
        """Метод для строкового отображения"""
        return self.name

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"
        ordering = ["name"]


class Lesson(models.Model):
    """Класс для уроков"""

    name = models.CharField(max_length=150, verbose_name="Название урока")
    description = models.TextField(
        max_length=300, verbose_name="Описание урока", blank=True, null=True
    )
    preview = models.ImageField(
        upload_to="study/lessons/",
        verbose_name="Превью",
        blank=True,
        null=True,
        help_text="Превью курса",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        max_length=150,
        verbose_name="Курсы",
        related_name="lessons",
        blank=True,
        null=True,
    )
    url = models.URLField(verbose_name="Ссылка на видео", blank=True, null=True)

    def __str__(self):
        """Метод для строкового отображения"""
        return self.name

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "туроки"
        ordering = [
            "course",
            "name",
        ]
