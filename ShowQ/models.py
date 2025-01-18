from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #additional fields
    age = models.PositiveSmallIntegerField(null=True)
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
    gender = models.IntegerField(choices=GENDER_CHOICES, null=True)
    address = models.CharField(max_length= 255)
    phonenumber = models.IntegerField(null=True)
    mellicod = models.IntegerField(null=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __self__(self):
        return self.User.username

class Doctor(models.Model):

    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Schedule(models.Model):

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    start_date = models.DateField()
    start_time = models.TimeField()
    end_date = models.DateField()
    end_time = models.TimeField()
    days_of_week = models.BooleanField()
    appointment_length = models.IntegerField(help_text="Duration of each appointment in minutes")

    def __str__(self):
        return f"{self.doctor.name}'s Schedule from {self.start_date} to {self.end_date}"

class AppointmentsModel(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(to=Doctor, on_delete=models.CASCADE, related_name='appointments')
    date_time = models.DateTimeField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.name} on {self.date_time}"
    