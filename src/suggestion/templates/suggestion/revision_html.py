from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from suggestion.templates.dominate_tags import *


suggestion_url = \
    "{% url 'suggestion' request.goal.slug revision.suggestion.slug %}"


def result():
    with django_block("content") as content:
        goal_header()

        with div(_class="row small-gap-below"):
            column(4)
            with column(4):
                suggestion_image("{{ revision.title }}")

        with div(_class="row small-gap-below"):
            column(2)
            with column(8):
                with p():
                    text("This is a previous version of a ")
                    a("suggestion", href=suggestion_url)
                    text(" by {{ revision.suggestion.owner.name }}")
                text("{{ revision.description|markdown }}")

    return (
        "{% extends 'base.html' %}\n",
        "{% load staticfiles %}",
        "{% load humanize %}",
        "{% load markdown_deux_tags %}",
        content,
    )

# done123
