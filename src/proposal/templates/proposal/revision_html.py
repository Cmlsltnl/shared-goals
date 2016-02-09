from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from proposal.templates.dominate_tags import *


proposal_url = "{% url 'proposal' request.goal.slug proposal.slug %}"


def result():
    with django_block("content") as content:
        goal_header()

        with div(_class="row small-gap-below"):
            column(4)
            with column(4):
                proposal_image()

        with div(_class="row small-gap-below"):
            column(2)
            with column(8):
                with p():
                    text("This is a previous version of a ")
                    a("proposal", href=proposal_url)
                    text(" by {{ proposal.owner.name }}")
                text("{{ revision.description|markdown }}")

    return (
        "{% extends 'base.html' %}\n",
        "{% load staticfiles %}",
        "{% load humanize %}",
        "{% load markdown_deux_tags %}",
        content,
    )

# done123
