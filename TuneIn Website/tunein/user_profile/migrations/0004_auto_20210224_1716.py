# Generated by Django 3.1.5 on 2021-02-24 22:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_music'),
    ]

    operations = [
        migrations.AddField(
            model_name='music',
            name='albumID',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AddField(
            model_name='music',
            name='partOfAlbum',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='music',
            name='release_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 24, 17, 16, 56, 829272)),
        ),
    ]
