# Generated by Django 5.0.2 on 2024-02-25 12:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app01", "0002_alter_music_rank_alter_userinfo_age"),
    ]

    operations = [
        migrations.AddField(
            model_name="music",
            name="arrow",
            field=models.FileField(
                default="media/no.png",
                max_length=128,
                upload_to="arrow/",
                verbose_name="arrow",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="music",
            name="artist",
            field=models.CharField(
                blank=True, max_length=64, null=True, verbose_name="Artist"
            ),
        ),
        migrations.AddField(
            model_name="music",
            name="pic",
            field=models.FileField(
                blank=True,
                max_length=128,
                null=True,
                upload_to="album/",
                verbose_name="Logo",
            ),
        ),
        migrations.AddField(
            model_name="music",
            name="weeks",
            field=models.IntegerField(blank=True, null=True, verbose_name="Weeks"),
        ),
        migrations.AlterField(
            model_name="music",
            name="title",
            field=models.CharField(
                blank=True, max_length=64, null=True, verbose_name="Title"
            ),
        ),
    ]
