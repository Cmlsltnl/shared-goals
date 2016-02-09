from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text, raw

from goal.templates.dominate_tags import *

from proposal.templates.dominate_tags import *


load_reviews_js = """

$(document).ready(function() {
    $("#reviews").load(
        "{% url 'reviews' request.goal.slug proposal.slug %}",
        function() {
            $('div.rateit, span.rateit').rateit();
            $('#rateit-review').bind('rated', function() {
                $('#id_rating').val($(this).rateit('value'));
            });
        }
    );
});

"""


def result():
    with django_block("head") as head:
        script(
            src="{% static 'review/review.js' %}",
            type="text/javascript"
        )
        with script():
            raw(load_reviews_js)

    with django_block("content") as content:
        goal_header()

        with div(_class="row small-gap-below"):
            column(4)
            with column(4):
                proposal_image()

        with div(_class="row small-gap-below"):
            column(2)
            with column(8):
                h5(
                    "Published by {{ proposal.owner.global_user.name }}, "
                    "{{ proposal.pub_date|naturaltime }}"
                )
                text("{{ revision.description|markdown }}")

        div(id="reviews")

    return (
        "{% extends 'base.html' %}",
        "{% load staticfiles %}",
        "{% load markdown_deux_tags %}",
        "{% load humanize %}",
        head,
        content
    )

# done123
