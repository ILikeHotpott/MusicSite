# Generated by Django 4.2 on 2024-05-18 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0037_notificenter_userinfo_unread_count_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userinfo",
            name="unread_count",
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]