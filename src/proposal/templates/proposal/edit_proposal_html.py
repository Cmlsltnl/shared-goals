from django_dominate.django_tags import *

from dominate.tags import *

from dominate.util import text

from goal.templates.dominate_tags import *
from proposal.templates.dominate_tags import *


# 123
@form(
    method="post",
    id="proposal_form",
    enctype="multipart/form-data"
)
def proposal_form():
    django_csrf_token()
    with django_if("proposal_form"):
        with p():
            text("{{ proposal_form.cropping.errors }}")
            label(
                _for="{{ proposal_form.cropping.id_for_label }}",
                _class="form-label"
            )
            text("{{ proposal_form.cropping }}")

        with p():
            text("{{ proposal_form.image.errors }}")
            with label(
                _for="{{ proposal_form.image.id_for_label }}",
                _class="form-label"
            ):
                text("Image")
            text("{{ proposal_form.image }}")
            button("Upload", id="upload-submit", name="submit", value="upload")

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
            text("Describe your proposal")
        with textarea(
            name="description",
            form="proposal_form",
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
        text("{{ proposal_form.media }}")

    with django_block("content") as content:
        goal_header()

        column(2)
        with column(8):
            proposal_form()

    return (
        "{% extends 'base.html' %}\n",
        head,
        content,
    )
