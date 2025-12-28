# a_users/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', profile_view, name='profile'),                # matches: /profile/
    path('edit/', profile_edit_view, name="profile-edit"), # matches: /profile/edit/
    path('settings/', profile_settings_view, name="profile-settings"), # matches: /profile/settings/
    path('<username>/', profile_view, name='profile'),     # matches: /profile/bhavin/
]