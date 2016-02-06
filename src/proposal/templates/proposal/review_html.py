from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from proposal.templates.dominate_tags import *


def result():
    with django_block("head") as head:
        script(
            src="{% static 'proposal/proposal.js' %}",
            type="text/javascript"
        )

    with django_block("content") as content:
        goal_header()

        with div(_class="row small-gap-below"):
            column(4)
            with column(4):
                proposal_image()

        with div(_class="row small-gap-below"):
            column(2)
            with column(8):
                text("{{ version.description|markdown }}")

    return (
        "{% extends 'base.html' %}\n",
        "{% load staticfiles %}",
        "{% load markdown_deux_tags %}",
        head,
        content,
    )

# done
