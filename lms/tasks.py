from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_update_mail(course_name, subscriber_email):
    send_mail(
        subject=f"Курс {course_name} обновлен!",
        message=f"Теперь вам доступна обновленная версия курса {course_name}.",
        from_email=None,
        recipient_list=[subscriber_email],
    )
