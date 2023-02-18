from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User, Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Signal for creating a profile for every new user"""
    if created:
        Profile.objects.create(user=instance)
