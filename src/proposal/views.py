from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from goal.models import Goal, Member
from proposal.forms import ProposalForm, ProposalImageForm
from proposal.models import Proposal, Review, ProposalVersion


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
            draft_version = ProposalVersion()
            draft_version.save()

            draft = Proposal()
            draft.owner = member
            draft.goal = goal
            draft.current_version = draft_version
            draft.save()

            draft_version.proposal = draft
            draft_version.save()

        if request.method == 'POST':
            form = ProposalForm(request.POST, request.FILES)

            image_form = ProposalImageForm(request.POST, request.FILES)
            image_form_valid = image_form.is_valid()

            # always update title and description
            draft.current_version.title = form['title'].value()
            draft.current_version.description = form['description'].value()
            draft.current_version.save()

            # always update cropping
            if image_form_valid:
                draft.cropping = image_form.cleaned_data['cropping']

            if request.POST['submit'] == 'upload':
                if image_form_valid:
                    draft.image = image_form.cleaned_data['image']
                    draft.save()
            else:
                if image_form_valid and form.is_valid():
                    draft.slug = slugify(draft.current_version.title)
                    draft.is_draft = False
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
                initial=dict(
                    title=draft.current_version.title,
                    description=draft.current_version.description
                )
            )
            image_form = ProposalImageForm(
                initial=dict(cropping=draft.cropping),
                files=dict(image=draft.image)
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
        reviews = Review.objects.filter(proposal_version__proposal=proposal)
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
