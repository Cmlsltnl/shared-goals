from dominate.tags import *
from dominate.util import text
from django_dominate.django_tags import *
from goal.templates.dominate_tags import *


@form(method="post", action=".", id="proposal_form")
def proposal_form():
    django_csrf_token()
    with p():
        text("{{ form.title.errors }}")
        with label(_for="{{ form.title.id_for_label }}", _class="form-label"):
            text("Title")
        input_(
            id="id_title",
            type="text",
            name="title",
            maxlength="100",
            value="{{ form.title.value }}",
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

print("{% extends 'base.html' %}\n")

with django_block("content") as content:
    goal_header()
    proposal_form()
print(content)
