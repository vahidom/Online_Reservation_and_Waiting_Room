# Generated by Django 4.2.16 on 2025-01-14 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShowQ', '0014_schedulegpt_alter_schedule_service_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctorgpt2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('specialty', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Schedulegpt2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_date', models.DateField()),
                ('end_time', models.TimeField()),
                ('appointment_length', models.IntegerField(help_text='Duration of each appointment in minutes')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='ShowQ.doctor')),
            ],
        ),
    ]
