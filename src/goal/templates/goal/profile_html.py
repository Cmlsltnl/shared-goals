from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from suggestion.templates.dominate_tags import *


# 12
def result():
    with django_block("content") as content:
        goal_header()

        with div(_class="row"):
            with column(4):
                with h4(_class="small-gap-below"):
                    text("My suggestions:")

        with django_for("suggestion_list in suggestion_lists"):
            with div(_class="row small-gap-above"):
                with django_for("suggestion in suggestion_list"):
                    with column(4):
                        suggestion_list_item()
            with django_empty():
                h5("You have not created any suggestions yet")

    return (
        "{% extends 'base.html' %}\n",
        content,
    )
