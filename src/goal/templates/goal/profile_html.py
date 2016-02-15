from django.conf import settings
from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from suggestion.templates.dominate_tags import *


def result():
    with django_block("content") as content:
        goal_header()

        with div(_class="row"):
            with column(4):
                with h4(_class=""):
                    text("Your suggestions:")

        with django_for("suggestion_list in suggestion_lists"):
            with div(_class="row small-gap-above profile--suggestion-list"):
                with django_for("suggestion in suggestion_list"):
                    with column(2):
                        suggestion_list_item()
            with django_empty():
                h5("You have not created any suggestions yet")

        with div(_class="row"):
            with column(4):
                with h4(_class=""):
                    text("Notifications:")

        with django_for("notification in notifications"):
            with div(_class="row small-gap-above profile--suggestion-list"):
                text("{{ notification.html|safe }}")

        inline_script(settings.BASE_DIR, "goal/init_profile.js")

    return (
        "{% extends 'base.html' %}\n",
        content,
    )
