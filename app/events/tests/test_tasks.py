import json
import os
from unittest import mock
from django.test import TestCase
from django.conf import settings
from ..tasks import get_new_events
from ..models import Event


def event_search(fixture_name):
    with open(os.path.join(settings.BASE_DIR, f'events/test_fixtures/{fixture_name}.json')) as json_file:
        return json.load(json_file)


class GetNewEventsTaskTestCase(TestCase):

    @mock.patch('events.tasks.eventbrite.event_search', return_value=event_search('search_results'))
    @mock.patch('events.tasks.get_events_page.chunks')
    def test_get_new_events(self, mock_get_events_page_chunks, mock_event_search):
        get_new_events.apply()

        mock_get_events_page_chunks.assert_called_once()
        self.assertEqual(Event.objects.count(), 50)

    @mock.patch('events.tasks.eventbrite.event_search', side_effect=[event_search('search_results'),
                                                                     event_search('search_results2')])
    def test_get_new_events_n_get_events_page(self, mock_event_search):
        get_new_events.apply()

        self.assertEqual(Event.objects.count(), 100)
