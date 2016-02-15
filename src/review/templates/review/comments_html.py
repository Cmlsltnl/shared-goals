from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from suggestion.templates.dominate_tags import *


@div(_class="row")
def comment_header():
    column(2)
    with column(8):
        with div(
            id="sg-comment-{{ the_comment.pk }}",
            style="text-indent: {{ the_comment.indent }}px;"
        ):
            text("{{ the_comment.owner.name }}")
            with django_if("the_comment.reply_to"):
                text("(=> {{ the_comment.reply_to.owner.name }})")

            text(", {{ the_comment.pub_date|naturaltime }}")


@div(_class="row")
def comment_body():
    column(2)
    with column(8):
        with div(
            _class="comment--description",
            style="padding-left: {{ the_comment.indent }}px;"
        ):
            text("{{ the_comment.body }}")


@div(_class="row")
def reply_to_comment_link():
    comment_form_url = \
        "{% url 'reply_comment' request.goal.slug review.id the_comment.id %}"

    column(2)
    with column(8):
        a(
            "reply",
            _class="comment-reply-link",
            data_ajax_url=comment_form_url,
            style="padding-left: {{ the_comment.indent }}px;"
        )
        div(
            _class="comment-reply-div",
            style="padding-left: {{ the_comment.indent }}px;"
        )


@span()
def comment():
    comment_header()
    comment_body()
    with django_if("request.global_user"):
        reply_to_comment_link()


@span()
def review_comments():
    with django_for("the_comment in review.published_comments"):
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
