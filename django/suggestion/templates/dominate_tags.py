from django_dominate.django_tags import *

from dominate.tags import *


@div(
    _class="suggestion--image",
    style=(
        "{% if the_suggestion.image %}"
        "background-image:url({{ the_suggestion.image.url }});"
        "{% endif %}"
    )
)
def suggestion_image():
    div(_class="suggestion--gradient")
    with span(_class="suggestion--title"):
        span(
            "{{ the_suggestion.get_type_display }} {{ the_suggestion.stars }}",
            _class="title-caption"
        )
        h3("{{ the_revision.title }}")


def readonly_rateit(rating):
    return div(
        _class="rateit readonly-rateit",
        data_rateit_readonly="true",
        data_rateit_resetable="false",
        data_rateit_value=rating
    )
