from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from suggestion.templates.dominate_tags import *


@form(
    method="post",
    enctype="multipart/form-data",
    _class="small-gap-above"
)
def comment_form():
    django_csrf_token()

    with p():
        text("{{ comment_form.body.errors }}")
        with label(
            _for="{{ comment_form.body.id_for_label }}",
            _class="form-label"
        ):
            text("Reply to this comment")
        with textarea(
            name="body",
            _class="form-field"
        ):
            text("{{ comment_form.body.value }}")

    with div():
        button(
            "Submit",
            name="submit",
            value="save"
        )
        button(
            "Save draft",
            name="submit",
            value="cancel"
        )


def result():
    return (
        comment_form(),
    )
