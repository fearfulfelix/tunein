# Generated by Django 3.1.5 on 2021-02-18 01:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='account_type',
        ),
    ]
