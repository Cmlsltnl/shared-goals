from django_dominate.django_tags import *

from dominate.tags import *

from goal.templates.dominate_tags import *

from proposal.templates.dominate_tags import *


def result():
    with django_block("content") as content:
        goal_header()

        with django_for("proposal_list in proposal_lists"):
            with div(_class="row small-gap-above"):
                with django_for("proposal in proposal_list"):
                    with column(4):
                        proposal_list_item()
            with django_empty():
                h5("There are no proposals yet")

    return (
        "{% extends 'base.html' %}\n",
        content
    )
