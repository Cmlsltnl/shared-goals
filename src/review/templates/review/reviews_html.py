from django.conf import settings

from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from suggestion.templates.dominate_tags import *


#
@form(
    method="post",
    id="review-form",
    data_ajax_url=(
        "{% url 'reviews' request.goal.slug latest_revision.suggestion.slug %}"
    ),
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
            text("{{ post_button_header }}")
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
        text("{{ form.experience.errors }}")
        with label(
            _for="{{ form.experience.id_for_label }}",
            _class="form-label"
        ):
            text(
                "Do you have any experience with the suggested "
                "{{ latest_revision.suggestion.get_type_display }}?"
            )
        text("{{ form.experience }}")

    with p():
        text("{{ form.description.errors }}")
        with textarea(
            name="description",
            rows="10",
            _class="form-field"
        ):
            text("{{ form.description.value }}")

    with div():
        button(
            "{{ post_button_label }}",
            name="submit",
            value="save"
        )
        button(
            "{{ cancel_button_label }}",
            name="submit",
            value="cancel"
        )


revision_href = (
    "{% url 'revision' request.goal.slug "
    "published_review.revision.suggestion.slug published_review.revision.pk %}"
)


@div(_class="row big-gap-above")
def published_review():
    with div(_class="row"):
        column(2)
        with column(2):
            readonly_rateit("{{ published_review.rating }}")
        with column(6):
            with django_if(
                "published_review.revision.pk == latest_revision.pk"
            ):
                text("{{ published_review.header }}")
                with django_else():
                    text("A ")
                    with a(href=revision_href):
                        text("previous version")
                    text(" was {{ published_review.header|lowerfirst }}")

    comment_form_url = \
        "{% url 'post_comment' request.goal.slug published_review.id %}"

    with div(_class="row"):
        column(2)
        with column(8):
            with p():
                text("{{ published_review.description }}")

            with django_if("request.global_user"):
                a(
                    "comment on this review",
                    _class="comment-reply-link",
                    data_ajax_url=comment_form_url
                )
                div(_class="comment-reply-div")

    div(
        _class="comment-block",
        id=(
            "{% if published_review.id == review.id %}"
            "comments-on-my-review"
            "{% endif %}"
        ),
        data_ajax_url=(
            "{% url 'comments' request.goal.slug published_review.pk %}"
        )
    )


@div(_class="review--comments-notice tiny-gap-above")
def review_comments_notice():
    text("Note: updating your review will remove ")
    with a(href="#comments-on-my-review"):
        text("{{ review.published_comments|length }} related comments")


def result():
    with span() as reviews:
        with div(_class="row small-gap-below"):
            column(2)
            with column(8):
                with django_if("form"):
                    review_form()

                with django_if("review.published_comments|length"):
                    review_comments_notice()

        with django_for("published_review in published_reviews"):
            published_review()

        inline_script(settings.BASE_DIR, 'review/init_review_form.js')

    return (
        "{% load humanize %}",
        "{% load case_utils %}",
        reviews,
    )
