from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^ajax_reviews/(?P<proposal_slug>[\-\w]+)/$',
        views.ReviewsView.as_view(),
        name='reviews'
    ),
    url(
        r'^ajax_comments/(?P<review_id>\d+)/$',
        views.CommentsView.as_view(),
        name='comments'
    ),
    url(
        r'^ajax_post_comment/(?P<review_id>\d+)/$',
        views.PostCommentView.as_view(),
        name='post_comment'
    ),
    url(
        r'^ajax_reply_comment/(?P<review_id>\d+)/(?P<reply_to_comment_id>\d+)/$',
        views.PostCommentView.as_view(),
        name='reply_comment'
    ),
]
