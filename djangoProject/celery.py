from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

app = Celery('myproject')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'upload_music_ranks_every_day_at_noon': {
        'task': 'app01.tasks.task_upload_music_ranks_to_s3',
        'schedule': crontab(hour="12", minute="0"),
    },
    'update_music_ranks_every_day_after_noon': {
        'task': 'app01.tasks.task_update_music_ranks_from_s3',
        'schedule': crontab(hour="12", minute="5"),
    },
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
