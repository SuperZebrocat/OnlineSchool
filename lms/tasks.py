import datetime

from django.utils import timezone
from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail

from users.models import User


@shared_task
def send_update_mail(course_name, subscriber_email):
    send_mail(
        subject=f"Курс {course_name} обновлен!",
        message=f"Теперь вам доступна обновленная версия курса {course_name}.",
        from_email=None,
        recipient_list=[subscriber_email],
    )


@shared_task
def check_user_login():
    # users = User.objects.all()
    #
    # for user in users:
    #     if user.last_login is not None:
    #         month_after_last_login = user.last_login + timedelta(30)
    #         if month_after_last_login < timezone.now():
    #             user.is_active = False
    #             user.save()
    #             print(f"Пользователь {user.email} заблокирован")

    today = timezone.now().date()
    inactive_date = today - datetime.timedelta(days=30)

    User.objects.filter(
        is_active=True,
        is_staff=False,
        is_superuser=False,
        last_login__isnull=False,
        last_login__lt=inactive_date
    ).update(is_active=False)
