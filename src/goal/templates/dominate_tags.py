from django_dominate.django_tags import *

from dominate.tags import *


@div(_class="row big-gap-below")
def goal_header():
    with div(_class="text-center"):
        h1("{{ goal.title }}")
        with div(_class="button-grp"):
            button(
                "Top Proposals",
                _class="btn btn-default",
                onclick="location.href='{% url 'goal' goal.slug %}';"
            )
            button("Members", _class="btn btn-default")
            button(
                "My Profile",
                _class="btn btn-default",
                onclick="location.href='{% url 'profile' goal.slug %}';"
            )
