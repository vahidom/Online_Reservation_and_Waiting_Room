from django.shortcuts import render, redirect
from .forms import NewUserForm, ProfileForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from ShowQ.models import Doctor, Schedule, AppointmentsModel
from ShowQ.forms import AppointmentsForm
from django.views import generic, View
import datetime


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

class ScheduleDetailView(generic.DetailView):
    """
    A detail view part of the appointments view to show the detail of available
    time for each reservation
    """
    model = Schedule
    def date_range(self, start_date: datetime.date, end_date: datetime.date):
        days = int((end_date - start_date).days)+1
        for n in range(days):
            yield start_date + datetime.timedelta(n)
    
    def time_range(self, start_time:datetime.time, end_time: datetime.time, day: datetime.date, period:int):
        date_time = datetime.datetime.combine(day, start_time)
        for i in range(1,10):
            yield date_time + datetime.timedelta(minutes=period*i)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        startDate = self.object.start_date
        endDate = self.object.end_date
        startTime = self.object.start_time
        endtTime = self.object.end_time
        datetimelist = [ [time for time in self.time_range(startTime,endtTime,day, 5)] 
                        for day in self.date_range(startDate, endDate)]
        print("IN GET METHOD", datetimelist[0][0])
        context.update({'datetimelist': datetimelist})
        return context
        
class AppointmentsCreateView(generic.CreateView):
    """
    A crate view part of the appointments view to manage the user creating reservation time
    """
    template_name = "ShowQ/schedule_detail.html"
    form_class = AppointmentsForm
    model =  AppointmentsModel
    success_url = reverse_lazy('doclist')

    def post(self, request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = None
        reservation_model = AppointmentsModel(created_by=request.user, doctor= Doctor.objects.get(pk=self.kwargs['pk']),
                                               date_time= datetime.datetime.strptime(request.POST['apptime'], '%Y-%m-%d %H:%M:%S'))
        reservation_model.save()
        return super().post(request, *args, **kwargs)

class AppointmentsView(View):
    """
    This view bring the DetailView and FormView defined above together
    """
    def get(self, request, *args, **kwargs):
        view = ScheduleDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AppointmentsCreateView.as_view()
        return view(request, *args, **kwargs)
    

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