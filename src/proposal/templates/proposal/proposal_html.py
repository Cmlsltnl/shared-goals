from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from proposal.templates.dominate_tags import *


with django_block("head") as head:
    script(
        src="{% static 'proposal/proposal.js' %}",
        type="text/javascript"
    )


#
@form(
    method="post",
    action=".",
    id="review_form",
    enctype="multipart/form-data",
    _class="big-gap-above"
)
def review_form():
    django_csrf_token()
    with p():
        with label(
            _for="{{ form.rating.id_for_label }}",
            _class="form-label"
        ):
            text("Rate this proposal and give feedback")
        text("{{ form.rating.errors }}")
        input_(
            id="id_rating",
            type="hidden",
            name="rating",
            value="{{ form.rating.value }}",
            _class="form-field"
        )
        div(
            id="rateit-review",
            _class="rateit",
            data_rateit_resetable="false",
            data_rateit_value="{{ form.rating.value }}"
        )

    with p():
        text("{{ form.description.errors }}")
        with textarea(
            name="description",
            form="review_form",
            _class="form-field"
        ):
            text("{{ form.description.value }}")

    with div():
        button(
            "{{ post_button_label }}",
            id="save-submit",
            name="submit",
            value="save"
        )
        button("Cancel", id="cancel-submit", name="submit", value="cancel")

with django_block("content") as content:
    goal_header()

    with div(_class="row small-gap-below"):
        column(4)
        with column(4):
            with div(
                _class="proposal--photo",
                style="background-image:url({{ proposal.image.url }});",
                href="{% url 'proposal' goal.slug proposal.slug %}"
            ):
                div(_class="proposal--gradient")
                with h3(_class="proposal--title"):
                    text("{{ proposal.get_current_version.title }}")

    with div(_class="row"):
        column(2)
        with column(8):
            text("{{ proposal.get_current_version.description|markdown }}")
            review_form()

print("{% extends 'base.html' %}\n")
print("{% load staticfiles %}")
print("{% load markdown_deux_tags %}")

print(head)
print(content)

# done
