# Generated by Django 5.0.6 on 2024-07-08 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('material', '0003_lessons'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessons',
            name='video_url',
            field=models.URLField(blank=True, null=True, verbose_name='ссылка на видео'),
        ),
    ]
