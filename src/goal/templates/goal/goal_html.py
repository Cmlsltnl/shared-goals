from dominate.tags import *
from django_dominate.django_tags import *
from proposal.templates.dominate_tags import *
from goal.templates.dominate_tags import *


with django_block("content") as content:
    goal_header()
    proposal_columns()

    with django_for("proposal in proposals"):
        proposal_list()

print("{% extends 'base.html' %}\n")
print(content)
