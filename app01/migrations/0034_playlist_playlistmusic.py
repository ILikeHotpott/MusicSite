# Generated by Django 5.0.3 on 2024-05-06 07:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app01", "0033_moments_video_urls_alter_moments_image_urls"),
    ]

    operations = [
        migrations.CreateModel(
            name="Playlist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=128, verbose_name="Playlist Name"),
                ),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="Description"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created At"),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="playlists",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PlaylistMusic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "position",
                    models.PositiveIntegerField(
                        default=1, verbose_name="Track Position"
                    ),
                ),
                (
                    "music",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app01.music",
                        verbose_name="Music",
                    ),
                ),
                (
                    "playlist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tracks",
                        to="app01.playlist",
                        verbose_name="Playlist",
                    ),
                ),
            ],
            options={
                "ordering": ["position"],
                "unique_together": {("playlist", "music")},
            },
        ),
    ]