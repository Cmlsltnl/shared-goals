from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from suggestion.templates.dominate_tags import *


suggestion_url = \
    "{% url 'suggestion' request.goal.slug suggestion.slug %}"


def result():
    with django_block("content") as content:
        goal_header()

        with django_with("suggestion as the_suggestion"):
            with django_with("revision as the_revision"):
                with div(_class="row small-gap-below"):
                    column(4)
                    with column(4):
                        suggestion_image()

                with div(_class="row small-gap-below"):
                    column(2)
                    with column(8):
                        with p():
                            text("This is a previous version of a ")
                            a("suggestion", href=suggestion_url)
                            text(" by {{ the_suggestion.owner.name }}")
                        text("{{ the_revision.description|markdown }}")

    return (
        "{% extends 'base.html' %}\n",
        "{% load staticfiles %}",
        "{% load humanize %}",
        "{% load markdown_deux_tags %}",
        "{% load notification_tags %}",
        content,
    )

# done123
