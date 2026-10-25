from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from pkg.feature.models import Record


def _touch_side_effect(record):
    return record.name


@receiver(post_save, sender=Record, dispatch_uid="pkg.feature.record_created")
def on_record_created(sender, instance, created, **kwargs):
    if created:
        _touch_side_effect(instance)


@receiver(post_delete, sender=Record, dispatch_uid="pkg.feature.record_deleted")
def on_record_deleted(sender, instance, **kwargs):
    _touch_side_effect(instance)
