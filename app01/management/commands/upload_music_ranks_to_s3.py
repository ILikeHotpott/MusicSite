from django.core.management.base import BaseCommand
import boto3
import json
from datetime import datetime
import pytz
from django.conf import settings
from app01.utils.music_api import get_ranks_songs_artists


class Command(BaseCommand):
    """ Download music ranks and upload to Amazon S3 with daily folders """

    def handle(self, *args, **kwargs):
        adelaide_tz = pytz.timezone('Australia/Adelaide')
        today = datetime.now(adelaide_tz).strftime('%Y-%m-%d')
        region = "US"
        file_key = f'{today}-{region}/music_rankings.json'

        songs_info = get_ranks_songs_artists(100, region)
        # 确保数据是以JSON格式序列化
        data = json.dumps(songs_info)

        # 上传到S3
        s3 = boto3.resource('s3',
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        object = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, file_key)
        object.put(Body=data, ContentType='application/json')

        self.stdout.write(self.style.SUCCESS(f'Successfully uploaded music ranks to {file_key} in S3'))
