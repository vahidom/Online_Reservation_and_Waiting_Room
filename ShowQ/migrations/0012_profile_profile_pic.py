# Generated by Django 4.1.1 on 2023-04-09 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShowQ', '0011_delete_patients'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
    ]
