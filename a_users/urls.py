# a_users/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', profile_view, name='profile'),
    path('edit/', profile_edit_view, name="profile-edit"),
    path('settings/', profile_settings_view, name="profile-settings"),
    path('u/<username>/', profile_view, name='profile-user'),
    path('u/<username>/follow/', follow_toggle_view, name='follow-toggle'),
    path('notifications/dropdown/', notifications_dropdown_view, name='notifications-dropdown'),
    path('notifications/read-all/', notifications_mark_all_read_view, name='notifications-read-all'),
]