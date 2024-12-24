from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


BOOKING_PERIOD = (
    ("5", "5 دقیقه"),
    ("10", "10 دقیقه"),
    ("15", "15 دقیقه"),
    ("20", "20 دقیقه"),
    ("25", "25 دقیقه"),
    ("30", "30 دقیقه"),
    ("35", "35 دقیقه"),
    ("40", "40 دقیقه"),
    ("45", "45 دقیقه"),
)

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

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()