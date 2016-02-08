from django.shortcuts import render
from django.views.generic import View


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class GoalView(View):
    def get(self, request, goal_slug):
        proposals = request.goal.proposals.filter(
            is_draft=False
        ).order_by('-avg_rating')

        context = {
            'proposal_lists': chunks(proposals, 3)
        }
        return render(request, 'goal/goal.html', context)


class ProfileView(View):
    def get(self, request, goal_slug):
        proposals = request.goal.proposals.filter(
            owner=request.member,
            is_draft=False
        ).order_by('-avg_rating')

        context = {
            'proposal_lists': chunks(proposals, 3)
        }
        return render(request, 'goal/profile.html', context)
