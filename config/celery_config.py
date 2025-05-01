from __future__ import absolute_import, unicode_literals

import eventlet
eventlet.monkey_patch()  # noqa: E402

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('celery')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
