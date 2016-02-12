import glob
import importlib
import logging
import os
import re
import sys
import time

from django.core.management.base import BaseCommand
from django.conf import settings
# from django.core.management.base import CommandError

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def is_python_file(path):
    return True if re.search(r'.(py|js)$', path) else False


class EventHandler(FileSystemEventHandler):
    """Logs all the events captured."""

    def __init__(self, path):
        self.path = path
        self.python_templates = []
        self.__rescan()
        self.__generate_templates()

    def __rescan(self):
        pattern = os.path.join(self.path, "**/*_html.py")
        self.python_templates = [
            x for x in glob.iglob(pattern, recursive=True)
        ]

    def __generate_templates(self):
        current_imports = list(sys.modules.keys())

        for template in self.python_templates:
            rel_path = os.path.splitext(
                os.path.relpath(template, self.path))[0]

            import_path = re.sub(os.path.sep, ".", rel_path)
            try:
                mod = importlib.import_module(import_path)
                outputfile = re.sub(r'_html\.py$', '.html', template)
                with open(outputfile, 'w') as of:
                    for line in mod.result():
                        of.write(str(line))
                        of.write(os.linesep)
            except Exception as e:
                print(e)

        for new_import in [
            x for x in sys.modules.keys() if x not in current_imports
        ]:
            del sys.modules[new_import]

    def on_moved(self, event):
        super(EventHandler, self).on_moved(event)
        if event.is_directory or is_python_file(event.src_path):
            self.__rescan()
            self.__generate_templates()

    def on_created(self, event):
        super(EventHandler, self).on_created(event)
        if event.is_directory or is_python_file(event.src_path):
            self.__rescan()
            self.__generate_templates()

    def on_deleted(self, event):
        super(EventHandler, self).on_deleted(event)
        pass

    def on_modified(self, event):
        super(EventHandler, self).on_modified(event)
        if is_python_file(event.src_path):
            self.__generate_templates()


class Command(BaseCommand):
    help = \
        'Regenerates foo.html files from foo_html.py ' \
        'whenever a python file changes'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        path = settings.BASE_DIR
        event_handler = EventHandler(path)
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
