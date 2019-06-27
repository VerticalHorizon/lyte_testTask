from rest_framework import serializers
from .models import Event, STATUSES, EVENT_SALES_STATUSES

__all__ = ['EventSerializer']


class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    local_created_at = serializers.DateTimeField(read_only=True)
    local_updated_at = serializers.DateTimeField(read_only=True)
    status = serializers.ChoiceField(choices=map(lambda x: x[1], STATUSES))
    event_sales_status = serializers.ChoiceField(choices=map(lambda x: x[1], EVENT_SALES_STATUSES))
    minimum_ticket_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    maximum_ticket_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    url = serializers.URLField()

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('id',)
        ordering = ['-start']
