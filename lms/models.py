from django.db import models

from config import settings


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса", help_text="Укажите название курса")
    preview_image = models.ImageField(
        upload_to="lms/previews",
        null=True,
        blank=True,
        verbose_name="Превью курса",
        help_text="Загрузите превью курса",
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание курса", help_text="Введите описание курса"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", null=True, blank=True
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название урока", help_text="Укажите название урока")
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание урока", help_text="Введите описание урока"
    )
    preview_image = models.ImageField(
        upload_to="lms/previews",
        null=True,
        blank=True,
        verbose_name="Превью урока",
        help_text="Загрузите превью урока",
    )
    video_url = models.URLField(max_length=200)
    course = models.ForeignKey(
        Course, related_name="lessons", on_delete=models.CASCADE, verbose_name="Курс", help_text="Выберите курс"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Владелец", null=True, blank=True
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
