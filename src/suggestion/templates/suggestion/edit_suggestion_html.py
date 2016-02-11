from django.conf import settings

from django_dominate.django_tags import *

from dominate.tags import *

from dominate.util import text

from goal.templates.dominate_tags import *
from suggestion.templates.dominate_tags import *


@form(
    method="post",
    id="suggestion_form",
    enctype="multipart/form-data"
)
def suggestion_form():
    django_csrf_token()
    with p():
        text("{{ revision_form.title.errors }}")
        with label(
            _for="{{ revision_form.title.id_for_label }}",
            _class="form-label"
        ):
            text("Title")
        input_(
            id="id_title",
            type="text",
            name="title",
            maxlength="100",
            value="{{ revision_form.title.value }}",
            _class="form-field"
        )

    with p():
        text("{{ revision_form.description.errors }}")
        with label(
            _for="{{ revision_form.description.id_for_label }}",
            _class="form-label"
        ):
            text("Describe your suggestion")
        with textarea(
            name="description",
            form="suggestion_form",
            rows="20",
            _class="form-field"
        ):
            text("{{ revision_form.description.value }}")

    with div():
        button(
            "{{ post_button_label }}",
            id="save-submit",
            name="submit",
            value="save"
        )
        button(
            "{{ cancel_button_label }}",
            id="cancel-submit",
            name="submit",
            value="cancel"
        )


def result():
    with django_block("head") as head:
        text("{{ suggestion_form.media }}")

    with django_block("content") as content:
        goal_header()

        column(2)
        with column(8):
            suggestion_form()

        inline_script(settings.BASE_DIR, "suggestion/init_suggestion_form.js")

    return (
        "{% extends 'base.html' %}",
        "{% load staticfiles %}",
        head,
        content,
    )
