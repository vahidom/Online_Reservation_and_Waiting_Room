from dis import show_code
from django.urls import path
from . import views

#TEMPLATE TAGING
app_name = 'ShowQ'
urlpatterns = [
    path('queue/', views.plist, name = 'plist'),
    path('appointment/', views.show_date_time, name = 'show_date_time'),
    path("register/", views.register_request, name="register"),
    path('user_login/',views.user_login,name='user_login'),
    ]