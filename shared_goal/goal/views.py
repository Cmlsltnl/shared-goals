from django.shortcuts import render
from django.views.generic import View
from .models import Goal


class GoalView(View):
    def get(self, request):
        goal = Goal.objects.all()[0]
        context = {
            'goal': goal,
            'proposals': goal.proposal_set.all()
        }
        return render(request, 'goal/goal.html', context)
