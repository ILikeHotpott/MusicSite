# Generated by Django 5.0.3 on 2024-08-10 11:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app01", "0045_alter_playlist_tracks_alter_playlistitem_spotify_uri"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="playlistitem",
            index=models.Index(
                fields=["spotify_uri"], name="app01_playl_spotify_636735_idx"
            ),
        ),
    ]