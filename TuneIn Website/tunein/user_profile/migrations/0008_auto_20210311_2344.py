# Generated by Django 3.1.5 on 2021-03-12 04:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0007_auto_20210311_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='release_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 11, 23, 44, 46, 896509)),
        ),
    ]
