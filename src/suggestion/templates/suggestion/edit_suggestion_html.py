from django_dominate.django_tags import *

from dominate.tags import *

from dominate.util import text

from goal.templates.dominate_tags import *
from suggestion.templates.dominate_tags import *


@form(
    method="post",
    enctype="multipart/form-data",
)
def suggestion_form():
    django_csrf_token()

    with p():
        with django_if("show_errors"):
            text("{{ form.type.errors }}")
        with label(
            _for="{{ form.type.id_for_label }}",
            _class="form-label"
        ):
            text(
                "Will you suggest a one-time Action, "
                "or a continuous Practice?"
            )
        text("{{ form.type }}")

    with p():
        with django_if("show_errors"):
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

    url_markdown = 'http://commonmark.org/help/'
    with p():
        with django_if("show_errors"):
            text("{{ form.description.errors }}")
        with label(
            _for="{{ form.description.id_for_label }}",
            _class="form-label"
        ):
            text("Describe your suggestion")

        with p(style="font-size: 10px;"):
            with a(href=url_markdown):
                text("Markdown syntax")
            text(" allowed")

        with textarea(
            name="description",
            rows="16",
            _class="form-field"
        ):
            text("{{ form.description.value }}")

    with django_if("show_image_form"):
        with div(_class="suggestion-form--image"):
            with p():
                with django_if("show_errors"):
                    text("{{ form.cropping.errors }}")
                label(
                    _for="{{ form.cropping.id_for_label }}",
                    _class="form-label"
                )
                text("{{ form.cropping }}")

            with p():
                with django_if("show_errors"):
                    text("{{ form.image.errors }}")
                with label(
                    _for="{{ form.image.id_for_label }}",
                    _class="form-label"
                ):
                    text(
                        "Make your suggestion look good by uploading an image")
                text("{{ form.image }}")
                button(
                    "Upload",
                    # todo reenable automatic upload
                    # _class="hidden",
                    id="upload-submit",
                    name="submit",
                    value="upload"
                )

    with p(_class="small-gap-above small-gap-below"):
        with label(
            _class="form-label"
        ):
            text("All done, press Submit to publish your suggestion")
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


def result():
    with django_block("head") as head:
        text("{{ form.media }}")

    with django_block("content") as content:
        goal_header()

        column(2)
        with column(8):
            suggestion_form()

    return (
        "{% extends 'base.html' %}",
        "{% load staticfiles %}",
        head,
        content,
    )
