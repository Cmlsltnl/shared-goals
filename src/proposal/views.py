from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from goal.models import Goal, Member
from proposal.forms import ProposalForm
from proposal.models import Proposal


class ProposalView(View):
    def get(self, request, goal_slug, proposal_slug=None):
        return self.handle(request, goal_slug, proposal_slug)

    def post(self, request, goal_slug, proposal_slug=None):
        return self.handle(request, goal_slug, proposal_slug)

    def handle(self, request, goal_slug, proposal_slug="new-proposal"):
        goal = get_object_or_404(Goal, slug=goal_slug)
        member = get_object_or_404(Member, user=request.user)

        if request.method == 'POST':
            form = ProposalForm(request.POST)
            if form.is_valid():
                p = Proposal()
                p.title = form.cleaned_data['title']
                p.description = form.cleaned_data['description']
                p.goal = goal
                p.owner = member
                p.save()

                return HttpResponseRedirect(
                    reverse(
                        'proposal',
                        kwargs=dict(goal_slug=goal.slug, proposal_slug=p.slug)
                    )
                )
        else:
            form = ProposalForm()

        proposal = (
            Proposal.objects.get(slug=proposal_slug) if proposal_slug
            else None
        )

        context = {
            'goal': goal,
            'proposal': proposal,
            'member': member,
            'form': form
        }
        return render(request, 'proposal/new_proposal.html', context)
