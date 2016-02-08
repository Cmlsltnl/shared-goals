from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text


def column(k, **argv):
    return div(_class="col-md-%d" % k, **argv)


@a(
    _class="proposal--photo",
    style="background-image:url({{ proposal.image.url }});",
    href="{% url 'proposal' request.goal.slug proposal.slug %}"
)
def proposal_list_item():
    div(_class="proposal--gradient")
    with h3(_class="proposal--title"):
        text("{{ proposal.get_current_revision.title }}")


@div(
    _class="proposal--photo",
    style="background-image:url({{ proposal.image.url }});",
    href="{% url 'proposal' request.goal.slug proposal.slug %}"
)
def proposal_image():
    div(_class="proposal--gradient")
    with h3(_class="proposal--title"):
        text("{{ revision.title }}")


def readonly_rateit(rating):
    return div(
        _class="rateit readonly-rateit",
        data_rateit_readonly="true",
        data_rateit_resetable="false",
        data_rateit_value=rating
    )
