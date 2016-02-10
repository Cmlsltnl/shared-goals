from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from proposal.templates.dominate_tags import *


@form(
    method="post",
    id="comment-form",
    enctype="multipart/form-data",
    _class="big-gap-above"
)
def comment_form():
    django_csrf_token()

    with p():
        text("{{ comment_form.body.errors }}")
        with label(
            _for="{{ comment_form.body.id_for_label }}",
            _class="form-label"
        ):
            text("Comment on this review")
        with textarea(
            name="body",
            form="comment-form",
            _class="form-field"
        ):
            text("{{ comment_form.body.value }}")

    with div():
        button(
            "Submit",
            id="comment-submit",
            name="submit",
            value="save"
        )
        button("Cancel", id="cancel-submit", name="submit", value="cancel")


def result():
    return (
        comment_form(),
    )
