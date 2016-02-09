from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text, raw

from goal.templates.dominate_tags import *

from proposal.templates.dominate_tags import *


@form(
    method="post",
    id="comment-form",
    enctype="multipart/form-data",
    _class="big-gap-above"
)
def comment_form():
    django_csrf_token()

    with p():
        text("{{ comment_form.body.errors }}")
        with label(
            _for="{{ comment_form.body.id_for_label }}",
            _class="form-label"
        ):
            text("Comment on this review")
        with textarea(
            name="body",
            form="comment-form",
            _class="form-field"
        ):
            text("{{ comment_form.body.value }}")

    with div():
        button(
            "Submit",
            id="comment-submit",
            name="submit",
            value="save"
        )
        button("Cancel", id="cancel-submit", name="submit", value="cancel")


@span(_class="small-gap-below")
def comment():
    with div(_class="row"):
        column(4)
        with column(4):
            text("{{ comment.owner.name }}, ")
            text("{{ comment.pub_date|naturaltime }}")

    with div(_class="row"):
        column(4)
        with column(4):
            with p():
                text("{{ comment.body }}")


revision_href = (
    "{% url 'revision' request.goal.slug "
    "published_review.revision.proposal.slug published_review.revision.pk %}"
)


@div(_class="row")
def review_comments():
    with django_for("comment in published_review.published_comments"):
        comment()


def result():
    with django_block("content") as content:
        with django_if("comment_form"):
            with div(_class="row"):
                column(2)
                with column(8):
                    comment_form()

    return (
        "{% load humanize %}",
        "{% load case_utils %}",
        content,
    )
