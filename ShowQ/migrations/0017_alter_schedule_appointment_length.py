# Generated by Django 4.2.16 on 2025-01-17 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShowQ', '0016_rename_service_time_schedule_appointment_length_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='appointment_length',
            field=models.IntegerField(help_text='Duration of each appointment in minutes'),
        ),
    ]