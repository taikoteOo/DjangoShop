from django.urls import path
from .views import register, log_in, log_out, user_profile, change_password, change_profile


app_name = 'users'
urlpatterns = [
    path('registration/', register, name='register'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('change-password/', change_password, name='change-password'),
    path('change-profile/', change_profile, name='change-profile'),
    path('profile/<int:pk>/', user_profile, name='profile'),

]