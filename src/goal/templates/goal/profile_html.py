from django.conf import settings
from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from suggestion.templates.dominate_tags import *


@span
def list_of_suggestions(empty_msg):
    with django_for("suggestion_list in the_suggestions|chunks:6"):
        with div(_class="row small-gap-below profile--suggestion-list"):
            with django_for("suggestion in suggestion_list"):
                with column(2):
                    suggestion_list_item()
        with django_empty():
            h5(empty_msg)


@span
def suggestions_for_goal():
    with div(_class="row"):
        with column(4):
            with h4(_class=""):
                text("Suggestions for {{ the_goal }}:")

    with django_with(
        "the_goal|suggestions_owned_by:global_user as "
        "the_suggestions"
    ):
        list_of_suggestions("No suggestions yet")


@span
def reviews_for_goal():
    with div(_class="row"):
        with column(4):
            with h4(_class=""):
                text("Reviews for {{ the_goal }}:")

    with django_with(
        "the_goal|suggestions_reviewed_by:global_user as "
        "the_suggestions"
    ):
        list_of_suggestions("No reviews yet")


def result():
    with django_block("content") as content:
        goal_header()

        with div(_class="row"):
            with column(4):
                with h4(_class=""):
                    text("Notifications:")

        with django_for("notification in notifications"):
            with div(_class="row small-gap-above profile--suggestion-list"):
                text("{{ notification.html|safe }}")
            with django_empty():
                h5("No notifications yet")

        with django_for("member in global_user.memberships.all"):
            with django_with("member.goal as the_goal"):
                with div(_class="sg-review-{% cycle 'even' 'odd' %}"):
                    suggestions_for_goal()
                    reviews_for_goal()

        inline_script(settings.BASE_DIR, "goal/init_profile.js")

    return (
        "{% extends 'base.html' %}",
        "{% load notification_tags %}",
        "{% load shared_goals_tags %}",
        content,
    )
