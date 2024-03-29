# Generated by Django 3.1.5 on 2021-02-18 20:40

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0002_remove_profile_account_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=32)),
                ('release_date', models.DateTimeField(default=datetime.datetime(2021, 2, 18, 15, 40, 45, 903155))),
                ('album_art', models.ImageField(upload_to='static/media/albumPictures')),
                ('genre', models.CharField(default='', max_length=20)),
                ('explicit', models.BooleanField(default=False)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
