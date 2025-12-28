from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.models import User

def profile_view(request, username=None):
    if username:
        # Kisi aur ki profile dekh rahe hain
        user_profile = get_object_or_404(User, username=username).profile
    else:
        # Apni profile dekh rahe hain
        if not request.user.is_authenticated:
            return redirect('account_login')
        user_profile = request.user.profile
        
    return render(request, 'a_users/profile.html', {'profile': user_profile})


@login_required
def profile_edit_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    form = ProfileForm(instance=profile)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
            
    return render(request, 'a_users/profile_edit.html', {'form': form, 'profile': profile})

@login_required
def profile_settings_view(request):
    return render(request, 'a_users/profile_settings.html')