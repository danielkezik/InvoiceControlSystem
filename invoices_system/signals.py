from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User as DjangoUser, Group
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=DjangoUser)
def create_user(sender, instance, created, **kwargs):
    if created:
        User.objects.create(user=instance)


@receiver(pre_save, sender=User)
def save_user(sender, instance, **kwargs):
    old_instance = User.objects.get(pk=instance.id)
    if instance.user_class == User.MODERATOR and old_instance.user_class != User.MODERATOR:
        moderator = Group.objects.get(name='Moderator')
        moderator.user_set.add(instance.user)
        instance.user.is_staff = True
        instance.user.save()
    elif instance.user_class != User.MODERATOR and old_instance.user_class == User.MODERATOR:
        moderator = Group.objects.get(name='Moderator')
        moderator.user_set.remove(instance.user)
        instance.user.is_staff = False
        instance.user.save()
