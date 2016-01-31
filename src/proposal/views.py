from django.shortcuts import render
from django.views.generic import View
from django.shortcuts import get_object_or_404
from goal.models import Goal, Member
from proposal.forms import ProposalForm
from proposal.models import Proposal


class NewProposalView(View):
    def get(self, request, goal_slug):
        goal = get_object_or_404(Goal, slug=goal_slug)
        member = get_object_or_404(Member, user=request.user)
        form = ProposalForm(request.POST)

        context = {
            'goal': goal,
            'member': member,
            'form': form
        }
        return render(request, 'proposal/new_proposal.html', context)

    def post(self, request, goal_slug):
        goal = get_object_or_404(Goal, slug=goal_slug)
        member = get_object_or_404(Member, user=request.user)
        form = ProposalForm(request.POST)

        if form.is_valid():
            p = Proposal()
            p.title = form.cleaned_data['title']
            p.description = form.cleaned_data['description']
            p.goal = goal
            p.owner = member
            p.save()
