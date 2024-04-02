# Generated by Django 4.0.10 on 2024-03-31 23:19

import User.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_customuser_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_photo',
            field=models.ImageField(blank=True, null=True, upload_to=User.models.upload_to),
        ),
    ]