from django_dominate.django_tags import *

from dominate.tags import *

from dominate.util import text

from goal.templates.dominate_tags import *


# 123
@form(
    method="post",
    action=".",
    id="proposal_form",
    enctype="multipart/form-data"
)
def proposal_form():
    django_csrf_token()
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
        text("{{ version_form.title.errors }}")
        with label(
            _for="{{ version_form.title.id_for_label }}",
            _class="form-label"
        ):
            text("Title")
        input_(
            id="id_title",
            type="text",
            name="title",
            maxlength="100",
            value="{{ version_form.title.value }}",
            _class="form-field"
        )

    with p():
        text("{{ version_form.description.errors }}")
        with label(
            _for="{{ version_form.description.id_for_label }}",
            _class="form-label"
        ):
            text("Describe your proposal")
        with textarea(
            name="description",
            form="proposal_form",
            _class="form-field"
        ):
            text("{{ version_form.description.value }}")

    with div():
        button("Submit", id="save-submit", name="submit", value="save")
        button("Cancel", id="cancel-submit", name="submit", value="cancel")

print("{% extends 'base.html' %}\n")

with django_block("head") as head:
    text("{{ proposal_form.media }}")
print(head)

with django_block("content") as content:
    goal_header()
    proposal_form()
print(content)
