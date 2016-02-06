from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from proposal.templates.dominate_tags import *


# 12
def result():
    with django_block("content") as content:
        goal_header()

        with div(_class="row"):
            with column(4):
                with h3(_class="small-gap-below"):
                    text("Your proposals:")

        with django_for("proposal_list in proposal_lists"):
            with div(_class="row"):
                with django_for("proposal in proposal_list"):
                    with column(4):
                        proposal_list_item()
            with django_empty():
                h5("You have not created any proposals yet")

    return (
        "{% extends 'base.html' %}\n",
        content,
    )
