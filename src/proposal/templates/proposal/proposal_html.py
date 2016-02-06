from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from proposal.templates.dominate_tags import *


#
@form(
    method="post",
    action=".",
    id="review_form",
    enctype="multipart/form-data",
    _class="big-gap-above"
)
def review_form():
    django_csrf_token()
    with p():
        with label(
            _for="{{ form.rating.id_for_label }}",
            _class="form-label"
        ):
            text("Rate this proposal and give feedback")
        text("{{ form.rating.errors }}")
        input_(
            id="id_rating",
            type="hidden",
            name="rating",
            value="{{ form.rating.value }}",
            _class="form-field"
        )
        div(
            id="rateit-review",
            _class="rateit",
            data_rateit_resetable="false",
            data_rateit_value="{{ form.rating.value }}"
        )

    with p():
        text("{{ form.description.errors }}")
        with textarea(
            name="description",
            form="review_form",
            _class="form-field"
        ):
            text("{{ form.description.value }}")

    with div():
        button(
            "{{ post_button_label }}",
            id="save-submit",
            name="submit",
            value="save"
        )
        button("Cancel", id="cancel-submit", name="submit", value="cancel")


other_review_href = \
    "{% url 'review' goal.slug proposal.slug other_review.pk %}"


@div(_class="row")
def other_review():
    with div(_class="row"):
        column(2)
        with column(2):
            readonly_rateit("{{ other_review.rating }}")
        with column(6):
            with django_if("other_review.version.pk == version.pk"):
                with django_else():
                    text("A ")
                    with a(href=other_review_href):
                        text("previous version")
                    text(" was ")

            text("{{ other_review.header }}")

    with div(_class="row"):
        column(2)
        with column(8):
            with p():
                text("{{ other_review.description }}")


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
                review_form()

        with django_for("other_review in other_reviews"):
            other_review()

    return (
        "{% extends 'base.html' %}\n",
        "{% load staticfiles %}",
        "{% load markdown_deux_tags %}",
        head,
        content
    )

# done1234
