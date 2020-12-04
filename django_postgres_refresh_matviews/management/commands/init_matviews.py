from django.core.management.base import BaseCommand

from django_postgres_refresh_matviews.utils import init_matviews


class Command(BaseCommand):

    def handle(self, *args, **options):
        init_matviews()
