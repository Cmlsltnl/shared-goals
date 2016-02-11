from django.conf import settings

from django_dominate.django_tags import *

from dominate.tags import *

from dominate.util import text

from goal.templates.dominate_tags import *
from suggestion.templates.dominate_tags import *


@form(
    method="post",
    enctype="multipart/form-data",
    id="revision-form"
)
def revision_form():
    django_csrf_token()
    with p():
        text("{{ form.title.errors }}")
        with label(
            _for="{{ form.title.id_for_label }}",
            _class="form-label"
        ):
            text("Title")
        input_(
            id="id_title",
            type="text",
            name="title",
            maxlength="100",
            value="{{ form.title.value }}",
            _class="form-field"
        )

    with p():
        text("{{ form.description.errors }}")
        with label(
            _for="{{ form.description.id_for_label }}",
            _class="form-label"
        ):
            text("Describe your suggestion")
        with textarea(
            name="description",
            form="revision-form",
            rows="20",
            _class="form-field"
        ):
            text("{{ form.description.value }}")

    with div():
        button(
            "{{ post_button_label }}",
            id="saverevision-submit",
            name="submit",
            value="save"
        )
        button(
            "{{ cancel_button_label }}",
            id="cancelrevision-submit",
            name="submit",
            value="cancel"
        )


url_suggestion_image = \
    "{% url 'new-suggestion-image' request.goal.slug draft_suggestion.id %}"


def result():
    with django_block("head") as head:
        text("{{ form.media }}")

    with django_block("content") as content:
        goal_header()

        column(2)
        with column(8):
            with django_if("show_image_form"):
                div(
                    id="suggestion-image-div",
                    data_ajax_url=url_suggestion_image
                )
            revision_form()

        inline_script(settings.BASE_DIR, "suggestion/edit_suggestion_init.js")

    return (
        "{% extends 'base.html' %}",
        "{% load staticfiles %}",
        head,
        content,
    )
