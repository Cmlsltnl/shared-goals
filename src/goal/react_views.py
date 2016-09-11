"""Views for react based presentation."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View

from rest_framework import serializers, viewsets

from .models import Goal


class GoalSerializer(serializers.ModelSerializer):  # noqa
    class Meta:  # noqa
        model = Goal
        fields = ('title', 'get_url', 'pk')


class GoalViewSet(viewsets.ModelViewSet):  # noqa
    queryset = Goal.objects.filter(is_draft=False)
    serializer_class = GoalSerializer


class GoalsView(View):
    """Show list of all goals."""

    def get(self, request):  # noqa
        return render(request, 'shared_goals/react_base.html', {})


class GoalView(View):
    """Show list of all goals."""

    def get(self, request, goal_slug):  # noqa
        context = {
            'goal': request.goal,
        }
        return render(request, 'react_goal/goal.jsx', context)


class ProfileView(View):  # noqa
    @method_decorator(login_required)
    def get(self, request, goal_slug, username):  # noqa
        context = {
        }
        return render(request, 'react_goal/profile.html', context)
