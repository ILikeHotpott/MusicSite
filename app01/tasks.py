from celery import shared_task
from django.core.management import call_command

# 在两个终端中分别运行这两行代码
# celery -A djangoProject worker --loglevel=info
# celery -A djangoProject beat --loglevel=info

# 手动测试
# python manage.py upload_music_ranks_to_s3
# python manage.py update_music_ranks_from_s3


@shared_task
def task_upload_music_ranks_to_s3():
    call_command('upload_music_ranks_to_s3')


@shared_task
def task_update_music_ranks_from_s3():
    call_command('update_music_ranks_from_s3')
