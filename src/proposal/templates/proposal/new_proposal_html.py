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
        text("{{ image_form.cropping.errors }}")
        label(
            _for="{{ image_form.cropping.id_for_label }}",
            _class="form-label"
        )
        text("{{ image_form.cropping }}")

    with p():
        text("{{ image_form.image.errors }}")
        with label(
            _for="{{ image_form.image.id_for_label }}",
            _class="form-label"
        ):
            text("Image")
        text("{{ image_form.image }}")
        button("Upload", id="upload-submit", name="submit", value="upload")

    with p():
        text("{{ form.title.errors }}")
        with label(_for="{{ form.title.id_for_label }}", _class="form-label"):
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
            text("Describe your proposal")
        with textarea(
            name="description",
            form="proposal_form",
            _class="form-field"
        ):
            text("{{ form.description.value }}")

    with div():
        button("Submit", id="save-submit", name="submit", value="save")
        button("Cancel", id="cancel-submit", name="submit", value="cancel")

print("{% extends 'base.html' %}\n")

with django_block("head") as head:
    text("{{ image_form.media }}")
print(head)

with django_block("content") as content:
    goal_header()
    proposal_form()
print(content)
