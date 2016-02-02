from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from goal.models import Goal, Member
from proposal.forms import ProposalForm
from proposal.models import Proposal, Review


class NewProposalView(View):
    def get(self, request, goal_slug):
        return self.handle(request, goal_slug)

    def post(self, request, goal_slug):
        return self.handle(request, goal_slug)

    def handle(self, request, goal_slug):
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
                        kwargs=dict(goal_slug=goal.slug)
                    )
                )
        else:
            form = ProposalForm()

        context = {
            'goal': goal,
            'member': member,
            'form': form
        }
        return render(request, 'proposal/new_proposal.html', context)


class ProposalView(View):
    def get(self, request, goal_slug, proposal_slug=None):
        goal = get_object_or_404(Goal, slug=goal_slug)
        proposal = get_object_or_404(Proposal, slug=proposal_slug)
        member = Member.objects.filter(user=request.user).first()
        reviews = Review.objects.filter(proposal=proposal)
        review = (
            reviews.filter(owner=member).first() if member
            else None
        )

        context = {
            'goal': goal,
            'proposal': proposal,
            'member': member,
            'review': review,
            'reviews': reviews,
        }
        return render(request, 'proposal/proposal.html', context)
