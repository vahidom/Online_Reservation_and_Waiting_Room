# Generated by Django 4.1.1 on 2022-10-14 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShowQ', '0005_alter_patients_wait_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patients',
            name='wait_time',
            field=models.DurationField(),
        ),
    ]
