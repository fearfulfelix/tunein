# Generated by Django 3.1.5 on 2021-04-07 02:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0017_auto_20210402_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='release_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 6, 22, 34, 7, 979669)),
        ),
    ]