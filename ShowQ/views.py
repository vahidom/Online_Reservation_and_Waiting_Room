from django.shortcuts import render, redirect
from .forms import NewUserForm, ProfileForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User

# Create your views here.
def index(request):
  return render(request, 'ShowQ/index.html')

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to index.
    return HttpResponseRedirect(reverse('index'))


def plist(request):
    patients_list = User.objects.all
    context = {'patients_list': patients_list}
    return render(request, 'ShowQ/plist.html', context)

def show_date_time(request):
    patients_list = User.objects.all
    context = {'patients_list': patients_list}
    return render(request, 'ShowQ/show_date_time.html', context)

def register_request(request):
  registered = False
  if request.method == "POST":
    user_form = NewUserForm(data=request.POST)
    profile_form = ProfileForm(data=request.POST)

    if user_form.is_valid() and profile_form.is_valid():
      user = user_form.save()
      user.set_password(user.password)
      user.save()

      profile = profile_form.save(commit=False)
      profile.user = user

      if 'profile_pic' in request.FILES:
        profile.profile_pic = request.FILES['profile_pic']

      profile.save()
      registered = True
      login(request, user)
      messages.success(request, "Registration successful." )
      return redirect("index")
    else:
      print(user_form.errors, profile_form.errors)  
    # messages.error(request, "Unsuccessful registration. Invalid information.")

  else:
    user_form = NewUserForm()
    profile_form = ProfileForm()
  
  return render (request=request, template_name="ShowQ/register.html", 
                 context={"register_form":user_form, 
                          "profile_form":profile_form, 
                          "registered": registered})

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their index.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'ShowQ/login.html', {})

@login_required
@transaction.atomic
def update_profile(request):
  if request.method == 'POST':
    user_form = NewUserForm(request.POST, instance=request.user)
    profile_form = ProfileForm(request.POST, instance=request.user.profile)
    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      messages.success(request, _('Your profile was successfully updated!'))
      return redirect('settings:profile')
    else:
      messages.error(request, _('Please correct the error below.'))
  else:
    user_form = NewUserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
  return render(request, 'ShowQ/register.html', {
    'user_form': user_form,
    'profile_form': profile_form
  })