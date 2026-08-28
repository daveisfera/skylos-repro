from django.db.models.signals import post_save
from django.dispatch import receiver

from django_signals_app.models import Item


@receiver(post_save, sender=Item)
def on_item_saved(sender, instance, **kwargs):
    _ = sender
    _ = instance
