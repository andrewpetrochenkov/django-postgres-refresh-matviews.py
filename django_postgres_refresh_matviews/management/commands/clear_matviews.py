from django.core.management.base import BaseCommand

from django_postgres_refresh_matviews.models import Matview


class Command(BaseCommand):

    def handle(self, *args, **options):
        Matview.objects.delete()
