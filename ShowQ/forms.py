from django import forms
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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