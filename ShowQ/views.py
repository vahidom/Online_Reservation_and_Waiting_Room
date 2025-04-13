from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm, ProfileForm, AppointmentsForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from ShowQ.models import Doctor, AppointmentsModel
from django.views import generic
from .utils import generate_available_times
from django.utils.timezone import make_aware, localtime
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

class AppointmentCreateView(generic.CreateView):

    model = AppointmentsModel
    form_class = AppointmentsForm
    template_name = 'ShowQ/appointment_create_form.html'
    success_url = reverse_lazy('ShowQ:doclist')

    def get_initial(self):
      return {'doctor': get_object_or_404(Doctor, pk=self.kwargs['pk'])}
        # initial = super().get_initial()
        # initial['doctor'] = get_object_or_404(Doctor, pk=self.kwargs['pk'])
        # if self.request.user.is_authenticated:
        #     initial['user'] = self.request.user
        # return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['doctor'] = get_object_or_404(Doctor, pk=self.kwargs['pk'])
        #kwargs['user'] = self.request.user if self.request.user.is_authenticated else 'Guest'
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = get_object_or_404(Doctor, pk=self.kwargs['pk'])
        # initial_data = {
        # "user": self.request.user if self.request.user.is_authenticated else "Guest",
        # "doctor": doctor,
        # }
        # Create form with initial values
        #form = self.form_class(initial=initial_data)

        schedules = doctor.schedules.all()
        available_dates = set()
        for schedule in schedules:
            slots = generate_available_times(schedule)
            available_dates.update(slots.keys())        

        days = sorted([d.strftime('%Y-%m-%d') for d in available_dates])
        context['days'] = days
        context['doctor'] = doctor
        context['today'] = datetime.date.today().strftime('%Y-%m-%d')
        return context
    
    def form_valid(self, form):
      selected_time = self.request.POST.get('selected_time')

      try:
        date_str, time_str = selected_time.split()
        combined = datetime.datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        time_slot = make_aware(combined)
      except Exception:
        return JsonResponse({'success': False, 'error': "Invalid datetime format"}, status=400)

      doctor = form.cleaned_data['doctor']
      if AppointmentsModel.objects.filter(doctor=doctor, date_time=time_slot).exists():
            return JsonResponse({'success': False, 'error': "That time slot is already taken"}, status=409)

      appointment = form.save(commit=False)
      appointment.user = self.request.user
      appointment.date_time = time_slot
      appointment.save()

      return JsonResponse({'success': True, 'message': "Appointment booked!"})


    def form_invalid(self, form):
        errors = {field: [str(err) for err in errs] for field, errs in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors}, status=400)

# AJAX view to fetch available & reserved times for a day
def load_times_for_day(request, doctor_id, day):
    print('Load times for day View is runnign')
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    schedules = doctor.schedules.all()
    selected_date = datetime.datetime.strptime(day, '%Y-%m-%d').date()

    available = []
    for schedule in schedules:
        slot_map = generate_available_times(schedule)
        slots = slot_map.get(selected_date, [])
        available.extend([t.strftime('%H:%M') for t in slots])

    reserved_qs = AppointmentsModel.objects.filter(doctor=doctor, date_time__date=selected_date)
    reserved = [localtime(a.date_time).strftime('%H:%M') for a in reserved_qs]
    print('Available Times:', available)
    print('Reserved Time:', reserved)
    return JsonResponse({
        'available': sorted(available),
        'reserved': reserved
    })

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
