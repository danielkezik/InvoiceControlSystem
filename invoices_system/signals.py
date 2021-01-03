from django.db.models.signals import post_save
from django.contrib.auth.models import User as DjangoUser
from django.dispatch import receiver
from .models import User


@receiver(post_save, sender=DjangoUser)
def create_user(sender, instance, created, **kwargs):
    if created:
        User.objects.create(user=instance)


@receiver(post_save, sender=DjangoUser)
def save_user(sender, instance, **kwargs):
    instance.invoice_user.save()