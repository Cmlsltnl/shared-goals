from django_dominate.django_tags import *

from dominate.tags import *


@div(_class="row small-gap-below")
def goal_header():
    with div(_class="text-center"):
        h1("{{ request.goal.title }}")
        with div(_class="button-grp"):
            button(
                "Suggestions",
                _class="btn btn-default",
                onclick="location.href='{% url 'goal' request.goal.slug %}';"
            )
            button("Members", _class="btn btn-default")
            with django_if("request.member"):
                button(
                    "My Profile",
                    _class="btn btn-default",
                    onclick=(
                        "location.href='"
                        "{% url 'profile' request.goal.slug %}';"
                    )
                )
