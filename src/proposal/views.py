from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.views.generic import View
from django.utils.decorators import method_decorator

from proposal.forms import CommentForm, RevisionForm, ProposalForm, ReviewForm
from proposal.models import Comment, Proposal, Review, Revision


def membership_required(view):
    def _wrapper(request, *args, **kw):
        if not request.member:
            return HttpResponseRedirect(
                reverse(
                    'register',
                    kwargs=dict(goal_slug=request.goal.slug)
                )
            )
        return view(request, *args, **kw)
    return _wrapper


class EditProposalView(View):
    def __get_or_create_draft(self, request):
        draft = Proposal.objects.filter(
            is_draft=True, owner=request.member
        ).first()

        if not draft:
            draft = Proposal()
            draft.owner = request.member
            draft.goal = request.goal
            draft.save()

            revision = Revision()
            revision.proposal = draft
            revision.save()
        return draft

    def __get_posted_forms(self, request, proposal):
        def is_duplicate_title(title):
            return proposal.goal.proposals.filter(
                Q(slug=slugify(title)) & ~Q(pk=proposal.pk)
            ).exists()

        revision_form = RevisionForm(request.POST, request.FILES)
        revision_form.is_duplicate_title = is_duplicate_title

        return (revision_form, ProposalForm(request.POST, request.FILES))

    def __get_populated_forms(self, request, proposal):
        proposal_form = ProposalForm(
            initial=proposal.__dict__,
            files=dict(image=proposal.image)
        )
        if 'image' in proposal_form.errors:
            del proposal_form.errors['image']
        return (
            RevisionForm(initial=proposal.get_current_revision().__dict__),
            proposal_form
        )

    def __update_proposal_and_save(self, proposal, request):
        revision_form, proposal_form = \
            self.__get_posted_forms(request, proposal)
        is_revision_form_valid = revision_form.is_valid()
        is_proposal_form_valid = proposal_form.is_valid()

        current_revision = proposal.get_current_revision()
        current_revision.title = revision_form['title'].value()
        current_revision.description = revision_form['description'].value()
        current_revision.save()

        if is_proposal_form_valid:
            if 'image' in request.FILES:
                proposal.image = proposal_form.cleaned_data['image']
            proposal.cropping = proposal_form.cleaned_data['cropping']

            if is_revision_form_valid and request.POST['submit'] == 'save':
                proposal.slug = slugify(proposal.get_current_revision().title)
                proposal.apply_cropping_to_image(replace_original=True)
                proposal.is_draft = False

            proposal.save()

        return is_revision_form_valid and is_proposal_form_valid

    def __create_new_revision(self, proposal, request):
        revision_form, _ = self.__get_posted_forms(request, proposal)

        is_revision_form_valid = revision_form.is_valid()
        if is_revision_form_valid:
            revision = Revision()
            revision.title = revision_form['title'].value()
            revision.description = revision_form['description'].value()
            revision.proposal = proposal
            revision.save()

        return is_revision_form_valid

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

    @method_decorator(membership_required)
    @method_decorator(login_required)
    def get(self, request, goal_slug, proposal_slug=""):
        return self.handle(request, goal_slug, proposal_slug)

    @method_decorator(membership_required)
    @method_decorator(login_required)
    def post(self, request, goal_slug, proposal_slug=""):
        return self.handle(request, goal_slug, proposal_slug)

    def handle(self, request, goal_slug, proposal_slug):
        proposal = (
            get_object_or_404(Proposal, slug=proposal_slug) if proposal_slug
            else self.__get_or_create_draft(request)
        )
        is_posting = request.method == 'POST'

        if is_posting:
            if proposal_slug:
                should_accept_data = request.POST['submit'] == 'cancel' or \
                    self.__create_new_revision(proposal, request)
            else:
                should_accept_data = \
                    self.__update_proposal_and_save(proposal, request)

            if request.POST['submit'] == 'cancel':
                return self.__on_cancel(request.goal.slug)
            elif request.POST['submit'] == 'save' and should_accept_data:
                return self.__on_save(request.goal.slug, proposal.slug)

        revision_form, proposal_form = (
            self.__get_posted_forms(request, proposal)
            if is_posting and request.POST['submit'] == 'save' else
            self.__get_populated_forms(request, proposal)
        )

        context = {
            'revision_form': revision_form,
            'proposal_form': proposal_form if proposal.is_draft else None,
            'cancel_button_label':
                "Save draft" if proposal.is_draft else "Cancel",
            'post_button_label':
                "Submit" if proposal.is_draft else "Update",
        }

        return render(request, 'proposal/edit_proposal.html', context)


class ProposalView(View):
    def __on_cancel_or_save(self, proposal):
        return HttpResponseRedirect(
            reverse(
                'proposal',
                kwargs=dict(
                    goal_slug=proposal.goal.slug,
                    proposal_slug=proposal.slug
                )
            )
        )

    def __get_or_create_review(self, request, revision, all_reviews):
        review = all_reviews.filter(owner=request.member).first()
        if not review:
            review = Review()
            review.owner = request.member
            review.revision = revision
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

    def __get_or_create_comment(self, request, review):
        draft = review.comments.filter(
            is_draft=True, owner=request.global_user).first()

        if not draft:
            draft = Comment()
            draft.owner = request.global_user
            draft.target = review
            draft.save()

        return draft

    def __update_comment_and_save(self, request, comment):
        form = CommentForm(request.POST, request.FILES)
        is_form_valid = form.is_valid()
        if is_form_valid:
            comment.body = form.cleaned_data['body']
            if request.POST['submit'] == 'save':
                comment.is_draft = False
            comment.save()

        return is_form_valid

    def get(self, request, goal_slug, proposal_slug):
        return self.handle(request, goal_slug, proposal_slug)

    @method_decorator(membership_required)
    @method_decorator(login_required)
    def post(self, request, goal_slug, proposal_slug):
        return self.handle(request, goal_slug, proposal_slug)

    def handle(self, request, goal_slug, proposal_slug):
        proposal = get_object_or_404(Proposal, slug=proposal_slug)
        revision = proposal.get_current_revision()
        all_reviews = Review.objects.filter(revision__proposal=proposal)
        review = (
            None if not request.member
            else self.__get_or_create_review(request, revision, all_reviews)
        )
        comment = (
            None if not request.global_user
            else self.__get_or_create_comment(request, review)
        )
        is_posting = request.method == 'POST'

        if is_posting:
            if request.POST['submit'] == 'comment':
                is_data_valid = self.__update_comment_and_save(
                    request, comment)
                if is_data_valid:
                    return self.__on_cancel_or_save(proposal)

            else:
                is_data_valid = self.__update_review_and_save(review, request)
                try_again = \
                    request.POST['submit'] == 'save' and not is_data_valid
                if not try_again:
                    return self.__on_cancel_or_save(proposal)

        review_form = (
            None if (not request.member or proposal.owner == request.member)
            else (
                ReviewForm(request.POST, request.FILES)
                if is_posting and not request.POST['submit'] == 'comment' else
                ReviewForm(initial=review.__dict__)
            )
        )

        comment_form = (
            None if (not request.global_user)
            else (
                CommentForm(request.POST, request.FILES)
                if is_posting and request.POST['submit'] == 'comment' else
                CommentForm(initial=comment.__dict__)
            )
        )

        published_reviews = \
            all_reviews.filter(is_draft=False).order_by('-pub_date')

        context = {
            'proposal': proposal,
            'revision': revision,
            'review': review,
            'post_button_header': (
                None if not review
                else (
                    "Rate this proposal and give feedback" if review.is_draft
                    else "Update your review of this proposal"
                )
            ),
            'post_button_label': (
                None if not review
                else (
                    "Submit" if review.is_draft else "Update"
                )
            ),
            'cancel_button_label': (
                None if not review
                else ("Save draft" if review.is_draft else "Cancel")
            ),
            'review_form': review_form,
            'comment_form': comment_form,
            'published_reviews': published_reviews,
        }
        return render(request, 'proposal/proposal.html', context)


class RevisionView(View):
    def get(self, request, goal_slug, proposal_slug, revision_pk):
        revision = get_object_or_404(Revision, pk=revision_pk)

        context = {
            'proposal': revision.proposal,
            'revision': revision,
        }
        return render(request, 'proposal/revision.html', context)
