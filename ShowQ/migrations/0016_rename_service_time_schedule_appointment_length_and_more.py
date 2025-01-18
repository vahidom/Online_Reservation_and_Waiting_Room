# Generated by Django 4.2.16 on 2025-01-17 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShowQ', '0015_doctorgpt2_schedulegpt2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schedule',
            old_name='service_time',
            new_name='appointment_length',
        ),
        migrations.AlterField(
            model_name='schedulegpt2',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='ShowQ.doctorgpt2'),
        ),
    ]
