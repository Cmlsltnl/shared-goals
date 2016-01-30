from django.shortcuts import render
from django.views.generic import View
from .models import Goal


class GoalView(View):
    def get(self, request, goal_slug):
        goal = Goal.objects.all()[0]

        context = {
            'goal': goal,
            'proposals': goal.proposal_set.order_by('-rating')
        }
        return render(request, 'goal/goal.html', context)


class ProfileView(View):
    def get(self, request, goal_slug):
        goal = Goal.objects.all()[0]

        context = {
            'goal': goal,
            'proposals': goal.proposal_set.order_by('-rating')
        }
        return render(request, 'goal/goal.html', context)
