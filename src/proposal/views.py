from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.views.generic import View

from goal.models import Goal, Member

from proposal.forms import ProposalForm, ProposalImageForm, ReviewForm
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
            ProposalForm(initial=draft.get_current_version().__dict__),
            ProposalImageForm(
                initial=draft.__dict__,
                files=dict(image=draft.image)
            )
        )

    def __update_draft_and_save(self, draft, request):
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
                draft.apply_cropping_to_image()
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
            is_data_valid = self.__update_draft_and_save(draft, request)

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
    def __publish_review(
        self, member, proposal, rating, description, existing_review
    ):
        if existing_review:
            existing_review.delete()

    def __on_cancel_or_save(self, goal_slug, proposal_slug):
        return HttpResponseRedirect(
            reverse(
                'proposal',
                kwargs=dict(
                    goal_slug=goal_slug,
                    proposal_slug=proposal_slug
                )
            )
        )

    def __get_or_create_review(self, member, version, all_reviews):
        review = all_reviews.filter(owner=member).first()
        if not review:
            review = Review()
            review.owner = member
            review.version = version
            review.save()

        return review

    def __update_review_and_save(self, review, request):
        form = ReviewForm(request.POST, request.FILES)
        is_form_valid = form.is_valid()
        if is_form_valid:
            review.rating = form.cleaned_data['rating']
            review.description = form.cleaned_data['description']

            if request.POST['submit'] == 'save':
                review.is_draft = False

            review.save()

        return is_form_valid

    def get(self, request, goal_slug, proposal_slug):
        return self.handle(request, goal_slug, proposal_slug)

    def post(self, request, goal_slug, proposal_slug):
        return self.handle(request, goal_slug, proposal_slug)

    def handle(self, request, goal_slug, proposal_slug):
        goal = get_object_or_404(Goal, slug=goal_slug)
        member = Member.objects.filter(user=request.user).first()
        proposal = get_object_or_404(Proposal, slug=proposal_slug)
        version = proposal.get_current_version()
        all_reviews = Review.objects.filter(version__proposal=proposal)
        review = self.__get_or_create_review(member, version, all_reviews)

        if request.method == 'POST':
            is_data_valid = self.__update_review_and_save(review, request)
            try_again = request.POST['submit'] == 'save' and not is_data_valid
            if not try_again:
                return self.__on_cancel_or_save(goal.slug, proposal.slug)

        form = (
            ReviewForm(request.POST, request.FILES) if request.method == 'POST'
            else ReviewForm(initial=review.__dict__)
        )

        other_reviews = all_reviews.filter(
            ~Q(pk=review.pk) & Q(is_draft=False)
        )

        context = {
            'goal': goal,
            'proposal': proposal,
            'version': version,
            'member': member,
            'review': review,
            'post_button_label': "Submit" if review.is_draft else "Update",
            'form': form,
            'other_reviews': other_reviews,
        }
        return render(request, 'proposal/proposal.html', context)
