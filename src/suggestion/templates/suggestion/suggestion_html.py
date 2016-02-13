from django.conf import settings

from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from suggestion.templates.dominate_tags import *


@div(_class="row small-gap-below")
def suggestion_image_div():
    column(4)
    with column(4):
        suggestion_image("{{ revision.title }}")


@div(_class="row small-gap-below")
def suggestion_description_div():
    column(2)
    with column(8):
        h5(
            "Published by {{ suggestion.owner.global_user.name }}, "
            "{{ suggestion.pub_date|naturaltime }}"
        )
        text("{{ revision.description|markdown }}")


@div(id="sg-review-list")
def empty_reviews_div():
    pass


def result():
    with django_block("content") as content:
        goal_header()
        suggestion_image_div()
        suggestion_description_div()
        empty_reviews_div()

        inline_script(settings.BASE_DIR, 'review/sg_comment_list.js')
        inline_script(settings.BASE_DIR, 'review/sg_review_list.js')
        inline_script(settings.BASE_DIR, 'suggestion/init_suggestion.js')

    return (
        "{% extends 'base.html' %}",
        "{% load staticfiles %}",
        "{% load markdown_deux_tags %}",
        "{% load humanize %}",
        content
    )
