from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

# 1. Jab naya user banega, tabhi profile banegi
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# 2. Jab user save hoga, toh uski profile ko bhi save (sync) karo
# Isme hum 'user.save()' call nahi karenge taaki loop na bane
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Agar kisi wajah se profile nahi bani, toh ab bana do
        Profile.objects.create(user=instance)