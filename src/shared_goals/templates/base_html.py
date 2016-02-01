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


url_new_proposal = "location.href='{% url 'new-proposal' goal.slug %}';"


@div(_class="row top-right-div")
def top_right_div():
    with div(_class="pull-right"):
        with django_if("user.is_authenticated"):
            with django_if("member"):
                with div(_class="btn-group btn-new-proposal"):
                    button(
                        "New Proposal",
                        _class="btn",
                        onclick=url_new_proposal
                    )
            top_right_menu()
            with django_else():
                with a(href="{% url 'auth_login' %}"):
                    text("{% trans 'Log in' %}")


with django_block("header") as header:
    top_right_div()

print("{% extends 'base_base.html' %}\n")
print("{% load i18n %}\n")
print(header)
