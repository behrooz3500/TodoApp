# Generated by Django 3.2.16 on 2023-02-16 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_auto_20230209_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcategory',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]