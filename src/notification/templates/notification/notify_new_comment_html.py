from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text


def result():
    with span() as content:
        with a(
            _class="sg-notification",
            data_next_url="{{ next_url }}",
        ):
            text("New comment from {{ comment.owner.name }} on your {{ on_what }}")

    return (
        content,
    )
