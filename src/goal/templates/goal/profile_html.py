from django_dominate.django_tags import *

from dominate.tags import *

from goal.templates.dominate_tags import *

from proposal.templates.dominate_tags import *

#
with django_block("content") as content:
    goal_header()

    h5("My proposals")
    proposal_columns()

    with django_for("proposal in proposals"):
        proposal_list_item()
        with django_empty():
            h5("You have not created any proposals yet")

print("{% extends 'base.html' %}\n")
print(content)
