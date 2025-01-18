from django.shortcuts import render, redirect
from .forms import NewUserForm, ProfileForm, AppointmentsForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from ShowQ.models import Doctor, AppointmentsModel
from django.views import generic
from .utils import generate_available_times
from django.utils.timezone import make_aware



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

class DocListView(generic.ListView):
    model = Doctor

class AppointmentCreateView(generic.CreateView):

    model = AppointmentsModel
    form_class = AppointmentsForm
    template_name = 'ShowQ/appointment_create_form.html'
    success_url = reverse_lazy('ShowQ:doclist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = Doctor.objects.get(pk = self.kwargs['pk'])
        initial_data = {
        "user": self.request.user if self.request.user.is_authenticated else "Guest",
        "doctor": doctor,
        }
        # Create form with initial values
        form = self.form_class(initial=initial_data)

        schedules = doctor.schedules.all()
        available_times = {}
        # Combine available times for all schedules
        for schedule in schedules:
            schedule_times = generate_available_times(schedule)
            for date, times in schedule_times.items():
                if date not in available_times:
                    available_times[date] = []
                available_times[date].extend(times)

        # Sort times for each date
        for date in available_times:
            available_times[date] = sorted(available_times[date])
        
        context.update({'available_times': available_times, 'form': form, 'doctor': doctor})
        return context
    
    def form_valid(self, form):
      doctor = form.cleaned_data['doctor']
      date_time = form.cleaned_data['date_time']
      messages.success(self.request, f"Appointment confirmed with Dr. {doctor} on {date_time}")
      return super(AppointmentCreateView,self).form_valid(form)


    def form_invalid(self, form):
        # Re-render the form with errors
        if self.request.user.is_authenticated :
          messages.error(self.request, "There was an error with your submission. Please check your input.")
        else:
           messages.error(self.request, "Please Log In first")
        return self.render_to_response(self.get_context_data(form=form))

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
