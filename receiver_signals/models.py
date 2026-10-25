"""Model + receiver on the model module (web-server playlist/recruiting shape)."""

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Item(models.Model):
    name = models.CharField(max_length=64)

    def touch(self):
        return self.name

    class Meta:
        app_label = "receiver_signals"


@receiver(post_delete, sender=Item, dispatch_uid="receiver_signals.item_deleted")
def on_item_deleted(sender, instance, **kwargs):
    # Live: connected via @receiver; nothing else calls this.
    _ = sender
    _ = instance
