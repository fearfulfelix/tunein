# Generated by Django 3.1.5 on 2021-03-12 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_auto_20210310_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='audio_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]