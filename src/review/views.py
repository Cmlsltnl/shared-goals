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

    def __update_review_and_save(self, review, form, submit):
        is_form_valid = form.is_valid()

        if 'rating' in form.cleaned_data:
            review.rating = form.cleaned_data['rating']
        if 'experience' in form.cleaned_data:
            review.experience = form.cleaned_data['experience']
        if 'description' in form.cleaned_data:
            review.description = form.cleaned_data['description']
        if is_form_valid and submit == 'save':
            review.is_draft = False

        review.comments.filter(is_draft=False).delete()
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

        submit = request.POST.get('submit', 'none')
        if submit == 'cancel' and review.is_draft:
            submit = 'save draft'

        if request.method == 'POST':
            bound_form = ReviewForm(request.POST, request.FILES)
            if submit in ('save', 'save draft'):
                self.__update_review_and_save(review, bound_form, submit)

        review_form = None
        if request.member and suggestion.owner != request.member:
            review_form = (
                bound_form
                if submit == 'save' else
                ReviewForm(instance=review)
            )
            if suggestion.type == Suggestion.TYPE_ACTION:
                review_form.fields['experience'].choices = \
                    tuple(list(Review.EXPERIENCE_CHOICES)[:-1])

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
    def __get_or_create_comment(
        self, global_user, review, reply_to_comment_id
    ):
        draft = review.comments.filter(
            is_draft=True,
            owner=global_user,
            review_id=review.id,
            reply_to_id=reply_to_comment_id
        ).first()

        if not draft:
            draft = Comment()
            draft.owner = global_user
            draft.review = review
            draft.reply_to_id = reply_to_comment_id
            draft.save()

        return draft

    def __update_comment_and_save(self, comment, form, submit):
        is_form_valid = form.is_valid()

        if 'body' in form.cleaned_data:
            comment.body = form.cleaned_data['body']
        if is_form_valid and submit == 'save':
            comment.is_draft = False

        comment.save()
        return is_form_valid

    @method_decorator(login_required)
    def get(self, request, goal_slug, review_id, reply_to_comment_id=None):
        review = get_object_or_404(Review, pk=review_id)
        comment = self.__get_or_create_comment(
            request.global_user, review, reply_to_comment_id)
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
            request.global_user, review, reply_to_comment_id)

        submit = request.POST['submit']
        bound_form = CommentForm(request.POST, request.FILES)
        is_data_valid = self.__update_comment_and_save(
            comment, bound_form, submit)

        if submit == 'save' and not is_data_valid:
            return HttpResponse(
                json.dumps({
                    'success': False,
                    'form': self.__render_form(review, bound_form)
                }),
                content_type="application/json"
            )

        return HttpResponse(
            json.dumps({
                'success': True,
            }),
            content_type="application/json"
        )
