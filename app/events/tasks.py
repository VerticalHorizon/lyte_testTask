import logging
from datetime import datetime
from decimal import Decimal
from django.conf import settings
from celery.schedules import crontab
from celery.task.base import periodic_task
from celery import shared_task
from glom import glom, Coalesce, SKIP
from eventbrite import Eventbrite
from eventbrite.exceptions import InternetConnectionError
from .models import Event


logger = logging.getLogger(__name__)


eventbrite = Eventbrite(settings.EVENTBRITE_OAUTH_TOKEN)


GATHERED_FIELDS = [{
    'id': 'id',
    'name': 'name.text',
    'description': 'description.text',
    'start': 'start.utc',
    'end': 'end.utc',
    'url': 'url',
    'created': 'created',
    'changed': 'changed',
    'published': Coalesce('published', default=None),
    'status': 'status',
    'organizer_name': 'organizer.name',
    'category_name': Coalesce('category.name', default=SKIP),
    'event_sales_status': 'event_sales_status.sales_status',
    'currency': 'currency',
    'minimum_ticket_price': Coalesce('ticket_availability.minimum_ticket_price.major_value', default='0.00'),
    'maximum_ticket_price': Coalesce('ticket_availability.maximum_ticket_price.major_value', default='0.00'),
}]


def get_page(page=1):
    events = eventbrite.event_search(**{
        'start_date.range_start': datetime.now().replace(microsecond=0).isoformat(),
        'location.latitude': settings.EVENTBRITE_SEARCH_LATITUDE,
        'location.longitude': settings.EVENTBRITE_SEARCH_LONGITUDE,
        'location.within': settings.EVENTBRITE_SEARCH_WITHIN,
        'include_adult_events': True,
        'include_unavailable_events': False,
        'include_all_series_instances': False,
    }, expand='organizer,category,event_sales_status,ticket_availability', page=page)

    res = {
        'events': glom(events['events'], GATHERED_FIELDS),
        'pagination': events['pagination'],
    }
    return res


@periodic_task(run_every=crontab(minute='*/1'),
               autoretry_for=(InternetConnectionError,),
               default_retry_delay=10,
               name='get_new_events',
               ignore_result=True)
def get_new_events():
    first_page = get_page()

    get_events_page.chunks(zip(range(1, first_page['pagination']['page_count'] + 1)), 10).apply_async()

    Event.objects.bulk_create([Event(**row) for row in first_page['events']], ignore_conflicts=True)


@shared_task(autoretry_for=(InternetConnectionError,),
             default_retry_delay=10,
             ignore_result=True)
def get_events_page(page):
    page = get_page(page)

    Event.objects.bulk_create([Event(**row) for row in page['events']], ignore_conflicts=True)
