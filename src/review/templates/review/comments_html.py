from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from suggestion.templates.dominate_tags import *


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

    comment_form_url = \
        "{% url 'reply_comment' request.goal.slug review.id comment.id %}"

    with div(_class="row"):
        column(2)
        with column(8):
            with div(style="text-indent: {{ comment.indent }}px;"):
                "{{ comment.body }}"
                with django_if("request.global_user"):
                    a(
                        "reply",
                        _class="comment-reply-link",
                        data_ajax_url=comment_form_url
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
