from django.core.management.base import BaseCommand
from django.core.management import call_command
from lms.models import Course, Lesson
from users.models import Payment


class Command(BaseCommand):
    help = 'Load all fixtures into the database'

    def handle(self, *args, **kwargs):
        Course.objects.all().delete()
        Lesson.objects.all().delete()
        Payment.objects.all().delete()

        call_command('loaddata', 'courses_fixture.json')
        call_command('loaddata', 'lessons_fixture.json')
        call_command('loaddata', 'payments_fixture.json')

        self.stdout.write(self.style.SUCCESS('Successfully loaded all fixtures'))