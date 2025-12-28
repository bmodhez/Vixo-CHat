from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('a_rtchat.urls')),
    path('accounts/', include('allauth.urls')),
    path('profile/', include('a_users.urls')),
]

# Media files setup (Images load karne ke liye zaroori hai)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)