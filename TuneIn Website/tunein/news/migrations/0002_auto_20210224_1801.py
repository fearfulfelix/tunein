# Generated by Django 3.1.5 on 2021-02-24 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='path/to/img'),
        ),
    ]
