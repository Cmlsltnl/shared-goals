from django_dominate.django_tags import *

from dominate.tags import *


def column(k, **argv):
    return div(_class="col-md-%d" % k, **argv)


@div(_class="row")
def proposal_columns():
    column(8)
    with column(1):
        h4("Rating")
    with column(2):
        h4("Published")


@div(_class="row proposal")
def proposal_list_item():
    with django_with("proposal.get_current_version as version"):
        column(2)
        with column(1):
            img(src="{{ proposal.image.url }}", height="75", width="75")
        with column(5):
            with a(href="{% url 'proposal' goal.slug proposal.slug %}"):
                h3("{{ version.title }}")
        with column(1):
            h4("{{ proposal.avg_rating }}")
        with column(2):
            h4("{{ version.pub_date|date:'d M Y' }}")
