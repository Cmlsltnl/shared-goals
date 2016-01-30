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
            'proposals': goal.proposal_set.order_by('-rating')
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
                owner=member
            ).order_by('-rating')
        }
        return render(request, 'goal/profile.html', context)


class NewProposalView(View):
    def get(self, request, goal_slug):
        goal = get_object_or_404(Goal, slug=goal_slug)
        member = get_object_or_404(Member, user=request.user)
        context = {
            'goal': goal,
            'member': member,
        }
        return render(request, 'goal/new_proposal.html', context)
