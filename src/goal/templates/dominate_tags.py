from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text


def column(k, **argv):
    return div(_class="col-md-%d" % k, **argv)


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
                with button(
                    _class="btn btn-default",
                    onclick=(
                        "location.href='{% url 'profile' %}';"
                    )
                ):
                    text("Profile")
                    with django_with(
                        "request.global_user.notifications|unread "
                        "as unread_notifications"
                    ):
                        with django_if("unread_notifications.count"):
                            text(" ({{ unread_notifications.count }})")
