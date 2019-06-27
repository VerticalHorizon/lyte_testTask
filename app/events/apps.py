from django.conf import settings
from django.apps import AppConfig
from elasticsearch_dsl import connections


class EventsConfig(AppConfig):
    name = 'events'

    def ready(self):
        from .documents import EventDocument

        connections.create_connection(hosts=[settings.ELASTICSEARCH_URL], timeout=20)

        EventDocument.init()
