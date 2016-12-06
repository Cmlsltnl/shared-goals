from django_dominate.django_tags import *

from dominate.tags import *

from dominate.util import text

from goal.templates.dominate_tags import *


@form(
    method="post",
    enctype="multipart/form-data",
)
def goal_form():
    django_csrf_token()

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

    with django_if("show_image_form"):
        with div(_class="goal-form--image"):
            text("{{ crop_settings|django_jcrop_widget }}")

            with p():
                with django_if("show_errors"):
                    text("{{ form.image.errors }}")
                with label(
                    _for="{{ form.image.id_for_label }}",
                    _class="form-label"
                ):
                    text(
                        "Upload an image to illustrate your goal")
                text("{{ form.image }}")
                button(
                    "Upload",
                    id="upload-submit",
                    name="submit",
                    value="upload"
                )

    with div():
        with div(_class="small-gap-above small-gap-below"):
            with label(
                _class="form-label"
            ):
                text("{{ submit_button_header }}")
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


def result():
    with django_block("head") as head:
        text("{{ form.media }}")

    with django_block("content") as content:
        with div(_class="row"):
            column(2)
            with column(8):
                goal_form()

        text("{% init_django_jcrop %}")

    return (
        "{% extends 'base.html' %}",
        "{% load django_jcrop_tags %}",
        head,
        content,
    )
