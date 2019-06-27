from django.db import models


__all__ = ['Event', 'STATUSES', 'EVENT_SALES_STATUSES']


STATUSES = [
    ('draft', 'DRAFT'),
    ('live', 'LIVE'),
    ('started', 'STARTED'),
    ('ended', 'ENDED'),
    ('completed', 'COMPLETED'),
    ('canceled', 'CANCELED'),
]

EVENT_SALES_STATUSES = [
    ('on_sale', 'ON_SALE'),
    ('not_yet_on_sale', 'NOT_YET_ON_SALE'),
    ('sales_ended', 'SALES_ENDED'),
    ('sold_out', 'SOLD_OUT'),
    ('unavailable', 'UNAVAILABLE'),
]


class EventsSignalManager(models.Manager):
    def bulk_create(self, items, **kwargs):
        from . import signals

        results = super().bulk_create(items, **kwargs)

        for res in results:
            signals.post_bulk_create.send(
                sender=res.__class__, instance=res
            )
        return results


class Event(models.Model):
    objects = EventsSignalManager()

    id = models.BigAutoField(verbose_name='ID', primary_key=True, auto_created=True)
    name = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    start = models.DateTimeField()      # UTC
    end = models.DateTimeField()        # UTC
    url = models.URLField()
    created = models.DateTimeField()    # UTC
    changed = models.DateTimeField()    # UTC
    published = models.DateTimeField(null=True)  # UTC
    status = models.CharField(
        max_length=9,
        choices=STATUSES,
        default=STATUSES[0][0],
    )
    organizer_name = models.CharField(max_length=250, null=True)
    category_name = models.CharField(max_length=250, null=True)
    event_sales_status = models.CharField(
        max_length=15,
        choices=EVENT_SALES_STATUSES,
        default=EVENT_SALES_STATUSES[-1][0],
    )
    currency = models.CharField(max_length=3)  # ISO 4217
    minimum_ticket_price = models.DecimalField(null=True, decimal_places=2, max_digits=7)
    maximum_ticket_price = models.DecimalField(null=True, decimal_places=2, max_digits=7)

    local_created_at = models.DateTimeField(auto_now_add=True)
    local_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} [Start: {self.start}]'
