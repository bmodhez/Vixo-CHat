from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.models import User
from django.http import HttpResponse

from a_users.models import Follow

try:
    from a_rtchat.models import Notification
except Exception:  # pragma: no cover
    Notification = None

def profile_view(request, username=None):
    if username:
        # Kisi aur ki profile dekh rahe hain
        profile_user = get_object_or_404(User, username=username)
        user_profile = profile_user.profile
    else:
        # Apni profile dekh rahe hain
        if not request.user.is_authenticated:
            return redirect('account_login')
        profile_user = request.user
        user_profile = request.user.profile

    followers_count = Follow.objects.filter(following=profile_user).count()
    following_count = Follow.objects.filter(follower=profile_user).count()
    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(follower=request.user, following=profile_user).exists()
        
    return render(request, 'a_users/profile.html', {
        'profile': user_profile,
        'profile_user': profile_user,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    })


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


@login_required
def follow_toggle_view(request, username: str):
    if request.method != 'POST':
        return redirect('profile-user', username=username)

    target = get_object_or_404(User, username=username)
    if target == request.user:
        return redirect('profile')

    rel = Follow.objects.filter(follower=request.user, following=target)
    if rel.exists():
        rel.delete()
        messages.success(request, f'Unfollowed @{target.username}')
    else:
        Follow.objects.create(follower=request.user, following=target)
        messages.success(request, f'Following @{target.username}')

        # Optional in-app notification: only if user is offline (best-effort)
        try:
            if Notification is not None:
                from a_rtchat.notifications import should_persist_notification

                should_store = should_persist_notification(user_id=target.id)

                if should_store:
                    Notification.objects.create(
                        user=target,
                        from_user=request.user,
                        type='follow',
                        preview=f"@{request.user.username} followed you",
                        url=f"/profile/u/{request.user.username}/",
                    )

                    # Realtime toast/badge via per-user notify WS
                    try:
                        from asgiref.sync import async_to_sync
                        from channels.layers import get_channel_layer

                        channel_layer = get_channel_layer()
                        async_to_sync(channel_layer.group_send)(
                            f"notify_user_{target.id}",
                            {
                                'type': 'follow_notify_handler',
                                'from_username': request.user.username,
                                'url': f"/profile/u/{request.user.username}/",
                                'preview': f"@{request.user.username} followed you",
                            },
                        )
                    except Exception:
                        pass
        except Exception:
            pass

    return redirect('profile-user', username=username)


@login_required
def notifications_view(request):
    # User requested: no separate notifications page.
    return redirect('home')


@login_required
def notifications_dropdown_view(request):
    if Notification is None:
        return HttpResponse('', status=200)

    notifications = list(
        Notification.objects.filter(user=request.user)
        .select_related('from_user')
        .order_by('-created')[:12]
    )
    return render(request, 'a_users/partials/notifications_dropdown.html', {
        'notifications': notifications,
    })


@login_required
def notifications_mark_all_read_view(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    if Notification is not None:
        try:
            Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        except Exception:
            pass
    return HttpResponse(status=204)