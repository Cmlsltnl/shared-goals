from dominate.tags import *
from dominate.util import text
from django_dominate.django_tags import *


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


url_update_suggestion = (
    "location.href='{% url 'update-suggestion' request.goal.slug "
    "suggestion.slug %}';"
)
url_new_suggestion = \
    "location.href='{% url 'new-suggestion' request.goal.slug %}';"


@div(_class="row top-right-div")
def top_right_div():
    with div(_class="pull-right"):
        with django_if("user.is_authenticated"):
            with django_if("request.member"):
                with div(id="top-right-div-inner", _class="btn-group"):
                    with django_if(
                        "suggestion and suggestion.owner == request.member"
                    ):
                        button(
                            "Update Suggestion",
                            _class="btn btn-info",
                            onclick=url_update_suggestion
                        )

                    button(
                        "New Suggestion",
                        _class="btn",
                        onclick=url_new_suggestion
                    )
            top_right_menu()
            with django_else():
                with a(href="{% url 'auth_login' %}"):
                    text("{% trans 'Log in' %}")


def result():
    with django_block("header") as header:
        top_right_div()

    return (
        "{% extends 'base_base.html' %}\n",
        "{% load i18n %}\n",
        header,
    )
