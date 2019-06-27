import sys

from django.core.management import BaseCommand

from app.celery import debug_task


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            debug_task.delay()
        except Exception:
            sys.exit(1)
