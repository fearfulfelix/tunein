# Generated by Django 3.1.5 on 2021-02-18 19:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_music'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='release_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 18, 14, 47, 44, 832884)),
        ),
    ]
