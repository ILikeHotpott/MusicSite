# Generated by Django 4.2.1 on 2024-03-30 11:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app01", "0031_momentcomment"),
    ]

    operations = [
        migrations.AddField(
            model_name="us_topmusic",
            name="album_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
