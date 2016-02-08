from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from proposal.templates.dominate_tags import *


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
def review():
    with div(_class="row"):
        column(2)
        with column(2):
            readonly_rateit("{{ review.rating }}")
        with column(6):
            text("{{ review.header }}")

    with div(_class="row"):
        column(2)
        with column(8):
            with p():
                text("{{ review.description }}")


@span(_class="small-gap-below")
def comment():
    with div(_class="row"):
        column(2)
        with column(8):
            text("{{ comment.owner.user.get_full_name }}, ")
            text("{{ comment.pub_date|naturaltime }}")

    with div(_class="row"):
        column(2)
        with column(8):
            with p():
                text("{{ comment.body }}")


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
                text("{{ revision.description|markdown }}")

        review()

        with django_for("comment in comments"):
            comment()

        with div(_class="row"):
            column(2)
            with column(8):
                comment_form()

    return (
        "{% extends 'base.html' %}\n",
        "{% load staticfiles %}",
        "{% load humanize %}",
        "{% load markdown_deux_tags %}",
        head,
        content,
    )

# done
