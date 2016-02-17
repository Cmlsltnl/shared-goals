from django.conf import settings
from django_dominate.django_tags import *

from dominate.tags import *
from dominate.util import text

from goal.templates.dominate_tags import *

from suggestion.templates.dominate_tags import *


goal_url = "{% url 'goal' the_goal.slug %}"


def suggestions_for_goal():
    def suggestion():
        url = "{% url 'suggestion' the_goal.slug the_suggestion.slug %}"
        with column(2) as result:
            with a(href=url):
                with django_with(
                    "the_suggestion.get_current_revision as the_revision"
                ):
                    suggestion_image()
        return result

    def list_of_suggestions():
        with django_for("the_chunk in the_suggestions|chunks:6") as result:
            with div(_class="row small-gap-below profile--suggestion-list"):
                with django_for("the_suggestion in the_chunk"):
                    suggestion()
            with django_empty():
                h5("No suggestions yet")
        return result

    with span() as result:
        with div(_class="row"):
            with column(4):
                with h4(_class=""):
                    text("Suggestions for ")
                    a("{{ the_goal }}", href=goal_url)

        with django_with(
            "the_goal|suggestions_by:global_user as "
            "the_suggestions"
        ):
            list_of_suggestions()
    return result


def reviews_for_goal():
    def review():
        with django_with("the_review.revision as the_revision") as result:
            with django_with("the_revision.suggestion as the_suggestion"):
                url = (
                    "{% url 'suggestion' the_goal.slug the_suggestion.slug %}"
                    "#sg-review-{{ the_review.pk }}"
                )
                with column(2) as result:
                    with a(href=url):
                        suggestion_image()
        return result

    def list_of_reviews():
        with django_for("the_chunk in the_reviews|chunks:6") as result:
            with div(_class="row small-gap-below profile--suggestion-list"):
                with django_for("the_review in the_chunk"):
                    review()
            with django_empty():
                h5("No reviews yet")
        return result

    with span() as result:
        with div(_class="row"):
            with column(4):
                with h4(_class=""):
                    text("Reviews for ")
                    a("{{ the_goal }}", href=goal_url)

        with django_with(
            "the_goal|reviews_by:global_user as the_reviews"
        ):
            list_of_reviews()
    return result


def suggestions_and_reviews():
    with django_for("the_member in global_user.memberships.all") as result:
        with django_with("the_member.goal as the_goal"):
            with div(_class="sg-review-{% cycle 'even' 'odd' %}"):
                suggestions_for_goal()
                reviews_for_goal()
    return result


def notifications():
    def header():
        with div(_class="row") as result:
            with column(4):
                with h4(_class=""):
                    text("Notifications:")
        return result

    def list_them():
        with django_for("the_notification in notifications") as result:
            with div(_class="row"):
                text("{{ the_notification.html|safe }}")
            with django_empty():
                h5("No notifications yet")
        return result

    with django_if("show_notifications") as result:
        header()
        list_them()
    return result


def user_name():
    return h2("{{ global_user.name }}")


def result():

    with django_block("content") as content:
        user_name()
        notifications()
        suggestions_and_reviews()
        inline_script(settings.BASE_DIR, "goal/init_profile.js")

    return (
        "{% extends 'base.html' %}",
        "{% load notification_tags %}",
        "{% load shared_goals_tags %}",
        content,
    )
