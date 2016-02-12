import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from django.utils.decorators import method_decorator

from goal.views import membership_required

from suggestion.models import Suggestion
from review.forms import CommentForm, ReviewForm
from review.models import Comment, Review


class ReviewsView(View):
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

    def get(self, request, goal_slug, suggestion_slug):
        return self.handle(request, goal_slug, suggestion_slug)

    @method_decorator(membership_required)
    @method_decorator(login_required)
    def post(self, request, goal_slug, suggestion_slug):
        return self.handle(request, goal_slug, suggestion_slug)

    def handle(self, request, goal_slug, suggestion_slug):
        suggestion = get_object_or_404(Suggestion, slug=suggestion_slug)
        latest_revision = suggestion.get_current_revision()
        all_reviews = Review.objects.filter(revision__suggestion=suggestion)
        review = (
            None
            if not request.member else

            self.__get_or_create_review(request, latest_revision, all_reviews)
        )
        is_saving = (
            request.method == 'POST' and
            request.POST['submit'] == 'save'
        )

        if request.method == 'POST':
            if is_saving or review.is_draft:
                is_data_valid = self.__update_review_and_save(review, request)

        review_form = (
            (
                ReviewForm(request.POST, request.FILES)
                if is_saving and not is_data_valid else
                ReviewForm(instance=review)
            )
            if request.member and suggestion.owner != request.member else
            None
        )

        published_reviews = \
            all_reviews.filter(is_draft=False).order_by('-pub_date')

        context = {
            'latest_revision': latest_revision,
            'review': review,
            'post_button_header': (
                None
                if not review else

                "Rate this suggestion and give feedback"
                if review.is_draft else

                "Update your review of this suggestion"
            ),
            'post_button_label': (
                None
                if not review else

                "Submit"
                if review.is_draft else

                "Update"
            ),
            'cancel_button_label': (
                None
                if not review else

                "Save draft"
                if review.is_draft else

                "Cancel"
            ),
            'form': review_form,
            'published_reviews': published_reviews,
        }
        return render(request, 'review/reviews.html', context)


class CommentsView(View):
    def get(self, request, goal_slug, review_id):
        review = get_object_or_404(Review, pk=review_id)
        context = {
            'review': review,
        }
        return render(request, 'review/comments.html', context)


class PostCommentView(View):
    def __get_or_create_comment(self, request, review, reply_to_comment_id):
        draft = review.comments.filter(
            is_draft=True,
            owner=request.global_user,
            review_id=review.id,
            reply_to_id=reply_to_comment_id
        ).first()

        if not draft:
            draft = Comment()
            draft.owner = request.global_user
            draft.review = review
            draft.reply_to_id = reply_to_comment_id
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

    @method_decorator(login_required)
    def get(self, request, goal_slug, review_id, reply_to_comment_id=None):
        review = get_object_or_404(Review, pk=review_id)
        comment = self.__get_or_create_comment(
            request, review, reply_to_comment_id)
        return self.__render_form(
            request, review, CommentForm(instance=comment))

    def __render_form(self, request, review, form):
        context = {
            'review': review,
            'comment_form': form,
        }
        return render(request, 'review/post_comment.html', context)

    @method_decorator(login_required)
    def post(self, request, goal_slug, review_id, reply_to_comment_id=None):
        review = get_object_or_404(Review, pk=review_id)
        comment = self.__get_or_create_comment(
            request, review, reply_to_comment_id)
        is_saving = request.POST['submit'] == 'save'
        is_data_valid = self.__update_comment_and_save(request, comment)

        if is_saving and not is_data_valid:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'form': self.__render_form(
                        review,
                        CommentForm(request.POST, request.FILES)
                    )
                }),
                content_type="application/json"
            )

        return HttpResponse(
            json.dumps({
                'success': True,
            }),
            content_type="application/json"
        )
