from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text


def result():
    with span() as content:
        with a(
            _class="sg-notification sg-notification-read-{{ is_read }}",
            href="{{ target_url }}",
        ):
            text(
                "{{ comment.owner.name }} {{ did_what }}"
            )

    return (
        content,
    )
