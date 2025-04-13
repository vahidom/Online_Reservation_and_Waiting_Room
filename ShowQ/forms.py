from django import forms
from .models import Profile, AppointmentsModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from collections import defaultdict
from django.http import HttpResponseRedirect, HttpResponse

class NewUserForm(UserCreationForm):
	password1 = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ("username","first_name", "last_name", "email", "password1", "password2")

	# def save(self, commit=True):
	# 	user = super(NewUserForm, self).save(commit=False)
	# 	user.email = self.cleaned_data['email']
	# 	if commit:
	# 		user.save()
	# 	return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("age", "gender", "address", "phonenumber", "mellicod", "profile_pic") 
        

class AppointmentsForm(forms.ModelForm): 
    class Meta:
        model = AppointmentsModel
        fields = ['doctor']

    def __init__(self, *args, **kwargs):
        doctor = kwargs.pop('doctor', None)	
        super().__init__(*args, **kwargs)
        if doctor:
            self.fields['doctor'].initial = doctor
            self.fields['doctor'].widget = forms.HiddenInput()
             
          
