from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text


def column(k, **argv):
    return div(_class="col-md-%d" % k, **argv)


@a(
    _class="proposal--photo",
    style="background-image:url({{ proposal.image.url }});",
    href="{% url 'proposal' goal.slug proposal.slug %}"
)
def proposal_list_item():
    div(_class="proposal--gradient")
    with h3(_class="proposal--title"):
        text("{{ proposal.get_current_version.title }}")
