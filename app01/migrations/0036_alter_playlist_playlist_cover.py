# Generated by Django 5.0.3 on 2024-05-06 09:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app01", "0035_playlist_playlist_cover_playlist_track_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="playlist",
            name="playlist_cover",
            field=models.ImageField(
                blank=True,
                default="playlist_cover/default.png",
                max_length=512,
                null=True,
                upload_to="playlist_cover/",
                verbose_name="playlist_cover",
            ),
        ),
    ]
