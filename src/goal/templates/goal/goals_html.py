from django_dominate.django_tags import *

from dominate.tags import *

from goal.templates.dominate_tags import *

from suggestion.templates.dominate_tags import *


@a(
    href="{% url 'goal' goal.slug %}"
)
def goal_list_item():
    with div(
        _class="goal--image",
        style=(
            "{% if goal.image %}"
            "background-image:url({{ goal.image.url }});"
            "{% endif %}"
        ),
    ):
        div(_class="goal--gradient")
        with span(_class="goal--title"):
            h3("{{ goal.title }}")


def result():
    with django_block("content") as content:
        with div(_class="text-center"):
            h1("Shared Goals")

        with django_for("goal_list in goals|chunks:3"):
            with div(_class="row small-gap-above"):
                with django_for("goal in goal_list"):
                    with column(4):
                        goal_list_item()
            with django_empty():
                h5("There are no goals yet")

    return (
        "{% extends 'base.html' %}",
        "{% load shared_goals_tags %}",
        content
    )
