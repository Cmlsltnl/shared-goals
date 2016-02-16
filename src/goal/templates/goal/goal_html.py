from django_dominate.django_tags import *

from dominate.tags import *

from goal.templates.dominate_tags import *

from suggestion.templates.dominate_tags import *


def result():
    with django_block("content") as content:
        goal_header()

        with django_for("suggestion_list in suggestions|chunks:3"):
            with div(_class="row small-gap-above"):
                with django_for("suggestion in suggestion_list"):
                    with column(4):
                        suggestion_list_item()
            with django_empty():
                h5("There are no suggestions yet")

    return (
        "{% extends 'base.html' %}",
        "{% load notification_tags %}",
        "{% load shared_goals_tags %}",

        content
    )
