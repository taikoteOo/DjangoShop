from django.urls import path
from .views import register, log_in, log_out, user_profile, change_password, change_profile, change_photo


app_name = 'users'
urlpatterns = [
    path('registration/', register, name='register'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
    path('profile/change-password/', change_password, name='change-password'),
    path('profile/<int:pk>/change-photo/', change_photo, name='change-photo'),
    path('profile/<int:pk>/change-profile/', change_profile, name='change-profile'),
    path('profile/<int:pk>/', user_profile, name='profile'),

]