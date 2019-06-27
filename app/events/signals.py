from django.dispatch import receiver, Signal
from .models import Event
from .documents import EventDocument


__all__ = ['post_bulk_create']


post_bulk_create = Signal(providing_args=['instance'])


@receiver(post_bulk_create, sender=Event)
def populate_es(sender, instance, **kwargs):
    EventDocument(instance).save()
