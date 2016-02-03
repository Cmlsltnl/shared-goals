from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from goal.models import Goal, Member
from proposal.forms import ProposalForm, ProposalImageForm
from proposal.models import Proposal, Review


class NewProposalView(View):
    def get(self, request, goal_slug):
        return self.handle(request, goal_slug)

    def post(self, request, goal_slug):
        return self.handle(request, goal_slug)

    def handle(self, request, goal_slug):
        goal = get_object_or_404(Goal, slug=goal_slug)
        member = get_object_or_404(Member, user=request.user)

        draft = Proposal.objects.filter(
            is_draft=True, owner=member
        ).first()
        if not draft:
            draft = Proposal()
            draft.owner = member
            draft.goal = goal
            draft.title = "Enter a title"
            draft.description = "Enter a description"
            draft.save()

        if request.method == 'POST':
            if request.POST['submit'] == 'upload':
                image_form = ProposalImageForm(request.POST, request.FILES)
                if image_form.is_valid():
                    draft.image = image_form.cleaned_data['image']
                    draft.save()

            else:
                form = ProposalForm(request.POST, request.FILES)
                if form.is_valid():
                    # todo save cropping
                    # draft.cropping = image_form.cleaned_data['cropping']
                    draft.title = form.cleaned_data['title']
                    draft.description = form.cleaned_data['description']
                    draft.save()

                    return HttpResponseRedirect(
                        reverse(
                            'proposal',
                            kwargs=dict(
                                goal_slug=goal.slug,
                                proposal_slug=draft.slug
                            )
                        )
                    )
        else:
            form = ProposalForm(
                dict(
                    title=draft.title,
                    description=draft.description
                )
            )
            image_form = ProposalImageForm(
                dict(),
                dict(
                    image=draft.image
                )
            )

        context = {
            'goal': goal,
            'member': member,
            'form': form,
            'image_form': image_form,
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
