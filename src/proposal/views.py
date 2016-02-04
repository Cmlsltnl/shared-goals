from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.views.generic import View

from goal.models import Goal, Member

from image_cropping.templatetags.cropping import cropped_thumbnail

from proposal.forms import ProposalForm, ProposalImageForm
from proposal.models import Proposal, Review, Version


class NewProposalView(View):
    def __get_or_create_draft(self, member, goal):
        draft = Proposal.objects.filter(
            is_draft=True, owner=member
        ).first()

        if not draft:
            draft = Proposal()
            draft.owner = member
            draft.goal = goal
            draft.save()

            version = Version()
            version.proposal = draft
            version.save()
        return draft

    def __get_posted_forms(self, request):
        return (
            ProposalForm(request.POST, request.FILES),
            ProposalImageForm(request.POST, request.FILES)
        )

    def __get_populated_forms(self, request, draft):
        return (
            ProposalForm(
                initial=dict(
                    title=draft.get_current_version().title,
                    description=draft.get_current_version().description
                )
            ),
            ProposalImageForm(
                initial=dict(cropping=draft.cropping),
                files=dict(image=draft.image)
            )
        )

    def __update_draft(self, draft, request):
        form, image_form = self.__get_posted_forms(request)
        is_form_valid = form.is_valid()
        is_image_form_valid = image_form.is_valid()

        current_version = draft.get_current_version()
        current_version.title = form['title'].value()
        current_version.description = form['description'].value()
        current_version.save()

        if is_image_form_valid:
            if 'image' in request.FILES:
                draft.image = image_form.cleaned_data['image']
            draft.cropping = image_form.cleaned_data['cropping']

            if is_form_valid and request.POST['submit'] == 'save':
                draft.slug = slugify(draft.get_current_version().title)
                draft.image = cropped_thumbnail(None, draft, "cropping")[1:]
                draft.is_draft = False

            draft.save()

        return is_form_valid and is_image_form_valid

    def __on_cancel(self, goal_slug):
        # todo redirect to previous page
        return HttpResponseRedirect(
            reverse(
                'goal',
                kwargs=dict(
                    goal_slug=goal_slug
                )
            )
        )

    def __on_save(self, goal_slug, proposal_slug):
        return HttpResponseRedirect(
            reverse(
                'proposal',
                kwargs=dict(
                    goal_slug=goal_slug,
                    proposal_slug=proposal_slug
                )
            )
        )

    def get(self, request, goal_slug):
        return self.handle(request, goal_slug)

    def post(self, request, goal_slug):
        return self.handle(request, goal_slug)

    def handle(self, request, goal_slug):
        goal = get_object_or_404(Goal, slug=goal_slug)
        member = get_object_or_404(Member, user=request.user)
        draft = self.__get_or_create_draft(member, goal)

        if request.method == 'POST':
            is_data_valid = self.__update_draft(draft, request)
            if request.POST['submit'] == 'cancel':
                return self.__on_cancel(goal.slug)
            elif request.POST['submit'] == 'save' and is_data_valid:
                return self.__on_save(goal.slug, draft.slug)

        is_posting = (
            request.method == 'POST' and request.POST['submit'] == 'save'
        )

        form, image_form = (
            self.__get_posted_forms(request) if is_posting else
            self.__get_populated_forms(request, draft)
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
        reviews = Review.objects.filter(version__proposal=proposal)
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
