from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

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


@span(_class="")
def comment():
    with div(_class="row"):
        column(2)
        with column(8):
            with div(style="text-indent: {{ comment.indent }}px;"):
                text("{{ comment.owner.name }}")
                with django_if("comment.reply_to"):
                    text("(=> {{ comment.reply_to.owner.name }}) ")

                text(", {{ comment.pub_date|naturaltime }}")

    with div(_class="row"):
        column(2)
        with column(8):
            with div(style="text-indent: {{ comment.indent }}px;"):
                text("{{ comment.body }}")
                a(
                    "reply",
                    id="reply-comment-{{ comment.id }}",
                    _class="comment-reply-link"
                )
                div(_class="comment-reply-div")


@span()
def review_comments():
    with django_for("comment in review.published_comments"):
        with django_if("forloop.first"):
            hr()
        comment()
        hr()


def result():
    return (
        "{% load humanize %}",
        "{% load case_utils %}",
        review_comments(),
    )
