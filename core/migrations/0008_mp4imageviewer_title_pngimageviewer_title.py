# Generated by Django 4.0.5 on 2022-07-20 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_pngimageviewer'),
    ]

    operations = [
        migrations.AddField(
            model_name='mp4imageviewer',
            name='title',
            field=models.CharField(default='goddess', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pngimageviewer',
            name='title',
            field=models.CharField(default='goddess', max_length=255),
            preserve_default=False,
        ),
    ]
