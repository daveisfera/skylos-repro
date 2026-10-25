"""@receiver handlers imported from AppConfig.ready() — P1.1 / #1068 regression."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from receiver_signals.models import Item


@receiver(post_save, sender=Item, dispatch_uid="receiver_signals.item_created")
def on_item_created(sender, instance, created, **kwargs):
    if created:
        instance.touch()
