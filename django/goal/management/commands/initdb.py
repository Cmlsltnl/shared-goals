from django.conf import settings
from django.core.management.base import BaseCommand
from django.core import management
# from django.core.management.base import CommandError


class Command(BaseCommand):
    help = (
        'Creates empty database tables'
    )

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        if settings.DATABASES['default']['NAME'] == ":memory:":
            management.call_command('migrate', '--run-syncdb')
        else:
            management.call_command('migrate', '--run-syncdb')
            management.call_command(
                'makemigrations', 'goal', 'suggestion', 'review')
            management.call_command('migrate', '--fake-initial')
