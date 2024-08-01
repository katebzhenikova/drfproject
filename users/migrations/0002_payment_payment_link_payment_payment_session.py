# Generated by Django 5.0.6 on 2024-07-31 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_link',
            field=models.URLField(blank=True, max_length=400, null=True, verbose_name='ссылка на оплату'),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_session',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='id сессии'),
        ),
    ]