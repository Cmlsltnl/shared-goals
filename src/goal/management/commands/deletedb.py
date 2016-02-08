import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = \
        'Populates the database with example proposals'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        os.unlink(os.path.join(settings.BASE_DIR, "db.sqlite3"))
        shutil.rmtree(os.path.join(settings.BASE_DIR, "goal/migrations"))
        shutil.rmtree(os.path.join(settings.BASE_DIR, "proposal/migrations"))
