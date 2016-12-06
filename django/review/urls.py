from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^ajax-reviews/(?P<suggestion_slug>[\-\w]+)/$',
        views.ReviewsView.as_view(),
        name='reviews'
    ),
    url(
        r'^ajax-comments/(?P<review_id>\d+)/$',
        views.CommentsView.as_view(),
        name='comments'
    ),
    url(
        r'^ajax-post_comment/(?P<review_id>\d+)/$',
        views.PostCommentView.as_view(),
        name='post_comment'
    ),
    url(
        r'^ajax-reply_comment/(?P<review_id>\d+)/'
        '(?P<reply_to_comment_id>\d+)/$',
        views.PostCommentView.as_view(),
        name='reply_comment'
    ),
]
