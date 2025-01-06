from django.contrib import admin

from .models import Profile, Doctor, Schedule, AppointmentsModel

admin.site.register(Profile)
admin.site.register(Doctor)
admin.site.register(Schedule)
admin.site.register(AppointmentsModel)
