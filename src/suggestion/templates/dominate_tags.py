from django_dominate.django_tags import *

from dominate.tags import *


@a(href="{% url 'suggestion' the_suggestion.goal.slug the_suggestion.slug %}")
def suggestion_list_item():
    suggestion_image("{{ the_suggestion.get_current_revision.title }}")


@div(
    _class="suggestion--image",
    style=(
        "{% if the_suggestion.image %}"
        "background-image:url({{ the_suggestion.image.url }});"
        "{% endif %}"
    )
)
def suggestion_image(title):
    div(_class="suggestion--gradient")
    with span(_class="suggestion--title"):
        span(
            "{{ the_suggestion.get_type_display }}",
            _class="title-caption"
        )
        h3(title)


def readonly_rateit(rating):
    return div(
        _class="rateit readonly-rateit",
        data_rateit_readonly="true",
        data_rateit_resetable="false",
        data_rateit_value=rating
    )
