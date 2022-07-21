from .models import MyUser
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=MyUser)
def default_to_non_active(sender, instance, created, **kwargs):
    if created:
        instance.is_active = False
        instance.save()