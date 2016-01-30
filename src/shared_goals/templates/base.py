from dominate.tags import *
from dominate.util import text
from django_tags import *

with django_block("header") as header:
    with div(_class="row"):
        with div(_class="pull-right"):
            with div(_class="btn-group btn-new-proposal"):
                button("New Proposal", _class="btn")
            with django_if("user.is_authenticated"):
                with div(_class="dropdown clearfix pull-right"):
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

                with django_else():
                    with a(href="{% url 'auth_login' %}"):
                        text("{% trans 'Log in' %}")

print("{% extends 'base_base.html' %}\n")
print("{% load i18n %}\n")
print(header)
