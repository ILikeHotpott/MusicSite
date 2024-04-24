# Generated by Django 4.2.1 on 2024-04-12 12:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app01", "0032_us_topmusic_album_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="moments",
            name="video_urls",
            field=models.JSONField(default=list, verbose_name="Video URLs"),
        ),
        migrations.AlterField(
            model_name="moments",
            name="image_urls",
            field=models.JSONField(default=list, verbose_name="Image URLs"),
        ),
    ]