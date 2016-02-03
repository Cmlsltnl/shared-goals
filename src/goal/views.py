from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import get_object_or_404
from .models import Goal, Member


class GoalView(View):
    def get(self, request, goal_slug):
        goal = get_object_or_404(Goal, slug=goal_slug)
        member = get_object_or_404(Member, user=request.user)
        context = {
            'goal': goal,
            'member': member,
            'proposals': goal.proposal_set.filter(
                is_draft=False
            ).order_by('-avg_rating')
        }
        return render(request, 'goal/goal.html', context)


class ProfileView(View):
    def get(self, request, goal_slug):
        goal = get_object_or_404(Goal, slug=goal_slug)
        member = get_object_or_404(Member, user=request.user)
        context = {
            'goal': goal,
            'member': member,
            'proposals': goal.proposal_set.filter(
                owner=member,
                is_draft=False
            ).order_by('-avg_rating')
        }
        return render(request, 'goal/profile.html', context)
