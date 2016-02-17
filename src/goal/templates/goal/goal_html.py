from django_dominate.django_tags import *

from dominate.tags import *

from goal.templates.dominate_tags import *

from suggestion.templates.dominate_tags import *


def result():
    with django_block("content") as content:
        goal_header()

        url = (
            "{% url 'suggestion' the_suggestion.goal.slug "
            "the_suggestion.slug %}"
        )
        with django_for("the_chunk in suggestions|chunks:3"):
            with div(_class="row small-gap-above"):
                with django_for("the_suggestion in the_chunk"):
                    with column(4):
                        with a(href=url):
                            with django_with(
                                "the_suggestion.get_current_revision "
                                "as the_revision"
                            ):
                                suggestion_image()

            with django_empty():
                h5("There are no suggestions yet")

    return (
        "{% extends 'base.html' %}",
        "{% load notification_tags %}",
        "{% load shared_goals_tags %}",

        content
    )
