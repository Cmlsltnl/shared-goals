from dominate.tags import *
from dominate.util import text

from django_dominate.django_tags import *

from goal.templates.dominate_tags import *


@div(_class="dropdown clearfix pull-right")
def top_right_menu():
    with a(
        _class="btn dropdown-toggle",
        data_toggle="dropdown",
        href="#"
    ):
        text("{{ user.first_name }}")

    span(_class="caret")
    with ul(_class="dropdown-menu"):
        with li():
            with a(href="{% url 'auth_logout' %}"):
                text("{% trans 'Log out' %}")
            with a(href="{% url 'auth_password_change' %}"):
                text("{% trans 'Change password' %}")


@div(_class="btn-group")
def suggestion_buttons():
    url_update_suggestion = (
        "location.href='{% url 'update-suggestion' request.goal.slug "
        "suggestion.slug %}';"
    )
    url_new_suggestion = \
        "location.href='{% url 'new-suggestion' request.goal.slug %}';"

    with django_if(
        "suggestion and suggestion.owner == request.global_user"
    ):
        with button(_class="btn btn-info", onclick=url_update_suggestion):
            text("Edit Suggestion")

    with button(_class="btn btn-success", onclick=url_new_suggestion):
        text("New Suggestion")


@div(_class="btn-group")
def goal_buttons():
    url_new_goal = \
        "location.href='{% url 'new-goal' %}';"

    url_join_goal = \
        "location.href='{% url 'join-goal' request.goal.slug %}';"

    with django_if("not request.goal"):
        with button(_class="btn btn-success", onclick=url_new_goal):
            text("New Goal")

    with django_if("request.goal and not request.member"):
        with button(_class="btn btn-success", onclick=url_join_goal):
            text("Join Goal")


@div(_class="pull-right")
def top_right_div():
    with django_if("user.is_authenticated"):

        with django_if("request.member"):
            suggestion_buttons()

        with django_if("request.global_user"):
            goal_buttons()

        top_right_menu()
        with django_else():
            with a(href="{% url 'auth_login' %}"):
                text("{% trans 'Log in' %}")


@div
def top_left_div():
    with a(href="{% url 'home' %}"):
        text("Shared Goals")

    with a(
        href="https://github.com/mnieber/shared-goals/blob/master/README.md"
    ):
        text("| About")

    with a(
        href="https://github.com/mnieber/shared-goals/blob/master/TERMS.md"
    ):
        text("| Terms")

    with a(href="https://github.com/mnieber/shared-goals/issues"):
        text("| Give feedback")


def result():
    with django_block("header") as header:
        with div(_class="row top-right-div"):
            with column(12):
                top_left_div()
                top_right_div()

    return (
        "{% extends 'base_base.html' %}\n",
        "{% load i18n %}\n",
        header,
    )
