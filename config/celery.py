from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


app = Celery('config')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_daily_report': {
        'task': 'your_app_name.tasks.send_daily_report',
        'schedule': crontab(hour=7, minute=0),  # каждый день в 7:00
    },
}

