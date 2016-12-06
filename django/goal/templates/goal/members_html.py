from django_dominate.django_tags import *

from dominate.tags import *

from goal.templates.dominate_tags import *

from suggestion.templates.dominate_tags import *


def result():
    with django_block("content") as content:
        goal_header()

        url = (
            "{% url 'profile' request.goal.slug "
            "the_member.global_user.user.username %}"
        )
        with django_for("the_member in members"):
            with div(_class="row small-gap-above"):
                with column(12):
                    with a(href=url):
                        text("{{ the_member.name }}")
            with django_empty():
                h5("There are no members yet")

    return (
        "{% extends 'base.html' %}",
        "{% load notification_tags %}",
        "{% load shared_goals_tags %}",

        content
    )
