from dominate.tags import *
from dominate.util import text
from django_dominate.django_tags import *
from proposal.templates.dominate_tags import *
from goal.templates.dominate_tags import *


@form(method="post", action=".", id="proposal_form")
def proposal_form():
    django_csrf_token()
    with p():
        with label(_for="id_title"):
            text("Title")
        input_(id="id_title", type="text", name="title", maxlength="254")

    with p():
        with label(_for="id_description"):
            text("Description")
        with textarea(name="description", form="proposal_form"):
            text("Enter text here...")

with django_block("content") as content:
    goal_header()
    proposal_form()


print("{% extends 'base.html' %}\n")
print(content)
