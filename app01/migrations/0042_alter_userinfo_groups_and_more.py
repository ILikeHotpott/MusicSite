# Generated by Django 5.0.3 on 2024-07-14 10:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app01", "0041_reactuser"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userinfo",
            name="groups",
            field=models.ManyToManyField(
                blank=True,
                help_text="The groups this user belongs to.",
                related_name="app01_userinfo_set",
                to="auth.group",
                verbose_name="groups",
            ),
        ),
        migrations.AlterField(
            model_name="userinfo",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="app01_userinfo_set",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
    ]
