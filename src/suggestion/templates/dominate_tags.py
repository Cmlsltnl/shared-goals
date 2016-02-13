from django_dominate.django_tags import *

from dominate.tags import *


def column(k, **argv):
    return div(_class="col-md-%d" % k, **argv)


@a(href="{% url 'suggestion' request.goal.slug suggestion.slug %}")
def suggestion_list_item():
    suggestion_image("{{ suggestion.get_current_revision.title }}")


@div(
    _class="suggestion--image",
    style=(
        "{% if suggestion.image %}"
        "background-image:url({{ suggestion.image.url }});"
        "{% endif %}"
    )
)
def suggestion_image(title):
    div(_class="suggestion--gradient")
    with span(_class="suggestion--title"):
        span(
            "{{ suggestion.get_type_display }}",
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
