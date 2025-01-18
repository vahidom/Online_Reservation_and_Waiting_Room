from dis import show_code
from django.urls import path
from . import views

#TEMPLATE TAGING
app_name = 'ShowQ'
urlpatterns = [
    path('queue/', views.plist, name = 'plist'),
    path('doclist/', views.DocListView.as_view(), name = "doclist"),
    path("doclist/<int:pk>/schedule/", views.AppointmentCreateView.as_view(), name = "schedule"),
    path("register/", views.register_request, name="register"),
    path('user_login/',views.user_login,name='user_login'),
    ]