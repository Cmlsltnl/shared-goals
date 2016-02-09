from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^ajax_reviews/(?P<proposal_slug>[\-\w]+)/$',
        views.ReviewsView.as_view(),
        name='reviews'
    ),
]
