from dominate.tags import *
from dominate.util import text
from django_dominate.django_tags import *
from goal.templates.dominate_tags import *


#
@form(method="post", action=".", id="proposal_form")
def rating_form():
    django_csrf_token()
    with p():
        text("{{ form.title.errors }}")
        with label(_for="{{ form.rating.id_for_label }}", _class="form-label"):
            text("Rating")
        input_(
            id="id_rating",
            type="text",
            name="rating",
            maxlength="3",
            value="{{ form.rating.value }}",
            _class="form-field"
        )

    with p():
        text("{{ form.description.errors }}")
        with label(
            _for="{{ form.description.id_for_label }}",
            _class="form-label"
        ):
            text("Description")
        with textarea(
            name="description",
            form="proposal_form",
            _class="form-field"
        ):
            text("{{ form.description.value }}")

    with div():
        button("Save", name="save", value="saved")
        button("Cancel", name="cancel", value="cancelled")

with django_block("content") as content:
    goal_header()
    h1("{{ proposal.title }}")
    text("{{ proposal.description|markdown }}")

    with django_thumbnail("proposal.image '100x100' crop='center' as im"):
        img(
            src="{{ im.url }}",
            width="{{ im.width }}",
            height="{{ im.height }}"
        )

    with django_if("review"):
        with django_else():
            rating_form()


print("{% extends 'base.html' %}\n")
print("{% load markdown_deux_tags %}")
print("{% load thumbnail %}")

print(content)

