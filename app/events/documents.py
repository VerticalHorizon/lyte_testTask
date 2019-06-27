from elasticsearch_dsl import Document, Date, Double, Keyword, Text
from .models import Event
from .serializers import EventSerializer


__all__ = ['EventDocument']


class EventDocument(Document):
    name = Text(analyzer='snowball', fields={'raw': Keyword()})
    organizer_name = Text(analyzer='snowball', fields={'raw': Keyword()})
    description = Text(analyzer='snowball')
    start = Date()
    end = Date()
    minimum_ticket_price = Double()
    maximum_ticket_price = Double()

    def __init__(self, model=None, **kwargs):
        if model:
            kwargs = {**self.Django.serializer_class(model).data, **kwargs}
            pk = kwargs.pop('id')
            super().__init__(meta={'id': pk}, **kwargs)
        else:
            super().__init__(**kwargs)

    class Index:
        name = 'event'
        settings = {
          "number_of_shards": 2,
        }

    class Django:
        queryset = lambda **kwargs: Event.objects.filter(**kwargs)[0]
        serializer_class = EventSerializer
