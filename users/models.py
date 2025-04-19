from django.db import models
from django.contrib.auth.models import AbstractUser

from lms.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    phone_number = models.CharField(
        max_length=35, verbose_name="Телефон", blank=True, null=True, help_text="Укажите номер телефона"
    )
    city = models.CharField(max_length=150, verbose_name="Город", blank=True, null=True, help_text="Укажите город")
    avatar = models.ImageField(
        upload_to="users/avatars/", verbose_name="Аватар", blank=True, null=True, help_text="Загрузите свой аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    CASH = "cash"
    TRANSFER = "transfer"

    PAYMENT_METHODS = [
        (CASH, "Наличные"),
        (TRANSFER, "Перевод на счет"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    payment_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, related_name="payment")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True, related_name="payment")
    amount = models.PositiveIntegerField(verbose_name="Сумма платежа", help_text="Укажите сумму платежа")
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHODS, verbose_name="Способ оплаты", help_text="Укажите способ оплаты"
    )
    session_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Id сессии", help_text="Укажите Id сессии"
    )
    link = models.URLField(
        max_length=400, blank=True, null=True, verbose_name="Ссылка на оплату", help_text="Укажите ссылку на оплату"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.payment_date} - {self.amount}"
