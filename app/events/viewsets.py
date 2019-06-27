import re
from datetime import datetime
from rest_framework import viewsets, status
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Event
from .serializers import EventSerializer
from .documents import EventDocument


__all__ = ['EventViewSet']


CONDITIONS = {
    '>': 'gt',
    '<': 'lt',
    '>=': 'gte',
    '<=': 'lte',
    '': 'eq',
}

FIELDS = [
    'local_created_at',
    'local_updated_at',
    'status',
    'event_sales_status',
    'minimum_ticket_price',
    'maximum_ticket_price',
    'url',
    'name',
    'description',
    'start',
    'end',
    'created',
    'changed',
    'published',
    'organizer_name',
    'category_name',
    'currency',
]


class EventViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   viewsets.GenericViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def search(self, request) -> Response:

        if not request.data:
            return Response({'message': 'Empty request!'}, status=status.HTTP_400_BAD_REQUEST)

        search = EventDocument.search()

        for k, v in {k: v for k, v in request.data.items() if k in ('name', 'organizer_name')}.items():
            search = search.query("match", **{k: v})

        # TODO: validation
        condition_token = {k: re.findall(r"(<=|>=|<|>)*(.*)", v)[0] for k, v in request.data.items()}
        for k, ct in condition_token.items():
            condition, token = ct
            if k in ('start', 'end',):
                search = search.filter('range', **{k: {CONDITIONS[condition]:
                                                           datetime.strptime(token, '%Y-%m-%d').isoformat()}})
            elif k in ('minimum_ticket_price', 'maximum_ticket_price',):
                search = search.filter('range', **{k: {CONDITIONS[condition]: token}})

        response = search.execute()

        if response.success() and response.hits:
            return Response({'message': 'OK', 'results': [{f: getattr(r, f, None) for f in FIELDS} for r in response]}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Nothing!'}, status=status.HTTP_404_NOT_FOUND)
