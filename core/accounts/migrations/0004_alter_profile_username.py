# Generated by Django 3.2.16 on 2023-01-23 17:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_alter_profile_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="username",
            field=models.CharField(default="84836", max_length=255, unique=True),
        ),
    ]
