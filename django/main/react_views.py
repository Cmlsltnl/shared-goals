"""React views."""

from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response

from review.react_views import ReviewView
from goal.react_views import GoalView
from goal.models import Goal, Member
from suggestion.models import Suggestion
from suggestion.react_views import SuggestionView, EditSuggestionView


class BundleView(APIView):  # noqa
    queryset = Goal.objects.all()

    def _get_flags(self, request, goal_slug, suggestion_slug):  # noqa
        if request.user.is_anonymous():
            member = None
        else:
            member = Member.lookup(request.user, goal_slug)

        owns_goal = member and Goal.objects.filter(
            slug=goal_slug, owner=member.global_user
        ).exists()
        owns_suggestion = (
            member and suggestion_slug != "none" and
            Suggestion.objects.filter(
                slug=suggestion_slug,
                owner=member.global_user,
                goal__slug=goal_slug,
            ).exists()
        )

        data = {
            'add_comment': not request.user.is_anonymous(),
            'is_member': True if member else False,
            'join_goal': not member and goal_slug != "none",
            'edit_goal': owns_goal,
            'edit_suggestion': owns_suggestion,
            'add_review': not owns_suggestion,
            'add_goal': goal_slug == "none"
        }

        return data

    def get(self, request, goal_slug, suggestion_slug):  # noqa
        flags = self._get_flags(request, goal_slug, suggestion_slug)

        goal_response = (
            GoalView().get(request, goal_slug).data
            if goal_slug != "none"
            else None
        )

        suggestion_response = (
            SuggestionView().get(request, goal_slug, suggestion_slug).data
            if suggestion_slug != "none"
            else None
        )

        new_suggestion_response = (
            EditSuggestionView().get(request, goal_slug).data
            if goal_slug != "none" and flags['is_member']
            else None
        )

        review_response = (
            ReviewView().get(request, goal_slug, suggestion_slug).data
            if suggestion_slug != "none" and flags['is_member']
            else None
        )

        data = {
            'goal': goal_response,
            'suggestion': suggestion_response,
            'new_suggestion': new_suggestion_response,
            'review': review_response,
            'flags': flags
        }

        return Response(data)

class HomeView(View):  # noqa
    def get(self, request):  # noqa
        return render(request, 'main/react_base.html', {})
