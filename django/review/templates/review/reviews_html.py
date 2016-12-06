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
            "Cancel",
            name="submit",
            value="cancel"
        )


@div(_class="row")
def published_review_header():
    revision_href = (
        "{% url 'revision' request.goal.slug "
        "the_review.revision.suggestion.slug the_review.revision.pk %}"
    )

    column(2)
    with column(2):
        readonly_rateit("{{ the_review.rating }}")

    with column(6):
        with django_if("the_review.description"):
            text("Review ")
            with django_else():
                text("Rating ")

        with django_if(
            "the_review.revision.pk != latest_revision.pk"
        ):
            text("of a ")
            with a(href=revision_href):
                text("previous version ")

        text("by {{ the_review.header }}")


@div(_class="row")
def published_review_description():
    column(2)
    with column(8):
        with div(_class="review--description"):
            text("{{ the_review.description }}")


@div(_class="row")
def reply_to_review_link():
    comment_form_url = \
        "{% url 'post_comment' request.goal.slug the_review.id %}"

    column(2)
    with column(8):
        a(
            "comment on this review",
            _class="comment-reply-link",
            data_ajax_url=comment_form_url
        )
        div(_class="comment-reply-div")


def published_review_comments():
    return div(
        _class="sg-comment-list",
        id=(
            "{% if the_review.id == review.id %}"
            "comments-on-my-review"
            "{% endif %}"
        ),
        data_ajax_url=(
            "{% url 'comments' request.goal.slug the_review.pk %}"
        )
    )


@div(_class=(
    "row small-gap-above small-gap-below sg-review "
    "sg-review-{% cycle 'even' 'odd' %}"),
    id="sg-review-{{ the_review.pk }}"
)
def published_review():
    published_review_header()
    published_review_description()
    with django_if("request.global_user"):
        reply_to_review_link()
    published_review_comments()


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

        with django_for("the_review in published_reviews"):
            published_review()

    return (
        "{% load humanize %}",
        "{% load notification_tags %}",
        reviews,
    )
