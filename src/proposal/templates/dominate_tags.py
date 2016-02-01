from dominate.tags import *
from django_dominate.django_tags import *


def col(k, **argv):
    return div(_class="col-md-%d" % k, **argv)


@div(_class="row")
def proposal_columns():
    col(8)
    with col(1):
        h4("Rating")
    with col(2):
        h4("Published")


@div(_class="row proposal")
def proposal_list():
    col(2)
    with col(1):
        img(src="{{ proposal.image_url }}", height="75", width="75")
    with col(5):
        with a(href="{% url 'proposal' goal.slug proposal.slug %}"):
            h3("{{ proposal.title }}")
    with col(1):
        h4("{{ proposal.rating }}")
    with col(2):
        h4("{{ proposal.pub_date|date:'d M Y' }}")
