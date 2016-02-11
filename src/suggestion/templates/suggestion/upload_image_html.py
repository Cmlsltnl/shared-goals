from django_dominate.django_tags import *

from dominate.tags import *

from dominate.util import text


@form(
    method="post",
    enctype="multipart/form-data",
    id="image-form",
    data_token="{{ csrf_token }}"
)
def image_form():
    django_csrf_token()
    with p():
        text("{{ form.cropping.errors }}")
        label(
            _for="{{ form.cropping.id_for_label }}",
            _class="form-label"
        )
        text("{{ form.cropping }}")

    with p():
        text("{{ form.image.errors }}")
        with label(
            _for="{{ form.image.id_for_label }}",
            _class="form-label"
        ):
            text("Image")
        text("{{ form.image }}")
        button(
            "Upload",
            # todo reenable automatic upload
            # _class="hidden",
            id="upload-submit",
            name="submit",
            value="upload"
        )


def result():
    return (
        "{% load staticfiles %}",
        image_form(),
    )
