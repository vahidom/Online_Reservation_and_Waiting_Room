# Generated by Django 4.1.1 on 2022-09-25 20:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ShowQ', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patients',
            name='wait_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Waiting_time(approx)'),
            preserve_default=False,
        ),
    ]