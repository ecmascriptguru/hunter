from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User
from ...apps.articles.models import Bucket


@receiver(post_save, sender=User)
def create_personal_bucket(sender, instance, created, **kwargs):
    if created:
        Bucket.objects.create(name="{}'s personal bucket".format(instance.username), user=instance)