import os
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = \
        'Populates the database with example suggestions'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        db_path = os.path.join(settings.BASE_DIR, "db.sqlite3")
        if os.path.exists(db_path):
            os.unlink(db_path)

        for d in ("goal", "suggestion", "review"):
            path = os.path.join(settings.BASE_DIR, "%s/migrations" % d)
            if os.path.exists(path):
                shutil.rmtree(path)
