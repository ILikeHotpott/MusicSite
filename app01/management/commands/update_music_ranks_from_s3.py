from django.core.management.base import BaseCommand
import boto3
import json
from datetime import datetime
import pytz
from django.conf import settings
from app01.models import US_TopMusic


class Command(BaseCommand):
    help = 'Update database with music ranks from Amazon S3'

    def handle(self, *args, **kwargs):
        adelaide_tz = pytz.timezone('Australia/Adelaide')
        today = datetime.now(adelaide_tz).strftime('%Y-%m-%d')
        print(today)
        region = "US"
        file_key = f'{today}-{region}/music_rankings.json'

        s3_client = boto3.client('s3',
                                 aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        try:
            response = s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_key)
            songs_info = json.loads(response['Body'].read().decode('utf-8'))

            US_TopMusic.objects.all().delete()

            # 使用新数据更新数据库
            for song_info in songs_info:
                # 歌曲信息现在是通过索引访问
                rank = song_info[0]
                title = song_info[1]
                artist = song_info[2]
                album_name = song_info[3]
                cover_url = song_info[4]

                US_TopMusic.objects.create(
                    title=title,
                    artist=artist,
                    rank=rank,
                    album_name=album_name,
                    cover_url=cover_url,
                    region=region
                )

            self.stdout.write(self.style.SUCCESS('Database updated with new music ranks successfully.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to update database: {e}'))
