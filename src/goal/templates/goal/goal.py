from dominate.tags import *
from django_dominate.django_tags import *
from proposal.templates.dominate_tags import *


@div(_class="row main-menu")
def goal_header():
    with div(_class="text-center"):
        h1("{{ goal.title }}")
        with div(_class="button-grp"):
            button("Top Proposals", _class="btn btn-default")
            button("Members", _class="btn btn-default")
            button(
                "My Profile",
                _class="btn btn-default",
                onclick="location.href='{% url 'index' goal.slug %}';"
            )


with django_block("content") as content:
    goal_header()
    proposal_columns()

    with django_for("proposal in proposals"):
        proposal_list()

print("{% extends 'base.html' %}\n")
print(content)
