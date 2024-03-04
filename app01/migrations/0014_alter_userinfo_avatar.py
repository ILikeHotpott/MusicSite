# Generated by Django 5.0 on 2024-03-01 07:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app01", "0013_userinfo_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userinfo",
            name="avatar",
            field=models.FileField(
                blank=True,
                max_length=256,
                null=True,
                upload_to="avatar/",
                verbose_name="avatar",
            ),
        ),
    ]
