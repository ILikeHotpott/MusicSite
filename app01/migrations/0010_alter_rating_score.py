# Generated by Django 5.0.2 on 2024-02-28 01:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app01", "0009_alter_music_total_score"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rating",
            name="score",
            field=models.FloatField(max_length=5, verbose_name="Score"),
        ),
    ]
