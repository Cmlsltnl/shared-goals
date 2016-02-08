from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from proposal.templates.dominate_tags import *


#
@form(
    method="post",
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


@form(
    method="post",
    id="comment_form",
    enctype="multipart/form-data",
    _class="big-gap-above"
)
def comment_form():
    django_csrf_token()

    with p():
        text("{{ form.body.errors }}")
        with label(
            _for="{{ form.body.id_for_label }}",
            _class="form-label"
        ):
            text("Comment on this review")
        with textarea(
            name="body",
            form="comment_form",
            _class="form-field"
        ):
            text("{{ form.body.value }}")

    with div():
        button(
            "Submit",
            id="save-submit",
            name="submit",
            value="save"
        )
        button("Cancel", id="cancel-submit", name="submit", value="cancel")


@span(_class="small-gap-below")
def comment():
    with div(_class="row"):
        column(4)
        with column(4):
            text("{{ comment.owner.global_user.name }}, ")
            text("{{ comment.pub_date|naturaltime }}")

    with div(_class="row"):
        column(4)
        with column(4):
            with p():
                text("{{ comment.body }}")


revision_href = \
    "{% url 'revision' goal.slug proposal.slug published_review.revision.pk %}"


@div(_class="row")
def published_review():
    with div(_class="row"):
        column(2)
        with column(2):
            readonly_rateit("{{ published_review.rating }}")
        with column(6):
            with django_if("published_review.revision.pk == revision.pk"):
                text("{{ published_review.header }}")
                with django_else():
                    text("A ")
                    with a(href=revision_href):
                        text("previous version")
                    text(" was {{ published_review.header|lowerfirst }}")

    with div(_class="row"):
        column(2)
        with column(8):
            with p():
                text("{{ published_review.description }}")

    with django_for("comment in published_review.published_comments"):
        comment()


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
                h5(
                    "Published by {{ proposal.owner.global_user.name }}, "
                    "{{ proposal.pub_date|naturaltime }}"
                )
                text("{{ revision.description|markdown }}")
                review_form()

        with django_for("published_review in published_reviews"):
            published_review()

        with div(_class="row"):
            column(2)
            with column(8):
                comment_form()

    return (
        "{% extends 'base.html' %}\n",
        "{% load staticfiles %}",
        "{% load markdown_deux_tags %}",
        "{% load humanize %}",
        "{% load case_utils %}",
        head,
        content
    )

# done1234
