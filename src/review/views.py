from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator

from goal.views import membership_required

from proposal.models import Proposal
from review.forms import CommentForm, ReviewForm
from review.models import Comment, Review


class ReviewsView(View):
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
        import pudb; pudb.set_trace()
        return self.handle(request, goal_slug, proposal_slug)

    def handle(self, request, goal_slug, proposal_slug):
        proposal = get_object_or_404(Proposal, slug=proposal_slug)
        latest_revision = proposal.get_current_revision()
        all_reviews = Review.objects.filter(revision__proposal=proposal)
        review = (
            None
            if not request.member else
            self.__get_or_create_review(request, latest_revision, all_reviews)
        )
        comment = (
            None
            if not request.global_user else
            self.__get_or_create_comment(request, review)
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
            None
            if not request.global_user
            else (
                CommentForm(request.POST, request.FILES)
                if is_posting and request.POST['submit'] == 'comment' else
                CommentForm(initial=comment.__dict__)
            )
        )

        published_reviews = \
            all_reviews.filter(is_draft=False).order_by('-pub_date')

        context = {
            'latest_revision': latest_revision,
            'review': review,
            'post_button_header': (
                None
                if not review else (
                    "Rate this proposal and give feedback"
                    if review.is_draft else
                    "Update your review of this proposal"
                )
            ),
            'post_button_label': (
                None
                if not review else
                "Submit" if review.is_draft else "Update"
            ),
            'cancel_button_label': (
                None
                if not review else
                "Save draft" if review.is_draft else "Cancel"
            ),
            'review_form': review_form,
            'comment_form': comment_form,
            'published_reviews': published_reviews,
        }
        return render(request, 'review/reviews.html', context)
