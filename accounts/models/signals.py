from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .profile_models import Profile
import os
import shutil
from django.db.models.signals import post_delete

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()


@receiver(post_delete, sender=User)
def delete_user_directory(sender, instance, **kwargs):
    user_directory = os.path.join('media', 'accounts', 'user_image', str(instance.id))
    if os.path.exists(user_directory):
        shutil.rmtree(user_directory)
