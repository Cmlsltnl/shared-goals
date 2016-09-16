"""Main urls."""

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.views import static

from goal.react_views import GoalListView, GoalView, NewGoalView
from suggestion.react_views import (
    SuggestionList,
    SuggestionView,
    EditSuggestionView,
    UploadSuggestionImageView
)
from review.react_views import ReviewView

from react_views import HomeView, BundleView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/goals$', GoalListView.as_view()),
    url(r'^api/new-goal$', NewGoalView.as_view()),
    url(
        r'^api/new-suggestion/(?P<goal_slug>[\-\w]+)$',
        EditSuggestionView.as_view()
    ),
    url(
        r'^api/edit-suggestion/(?P<goal_slug>[\-\w]+)' +
        '/(?P<suggestion_slug>[\-\w]+)$',
        EditSuggestionView.as_view()
    ),
    url(
        r'^api/upload-suggestion-image/(?P<goal_slug>[\-\w]+)$',
        UploadSuggestionImageView.as_view()
    ),
    url(
        r'^api/upload-suggestion-image/(?P<goal_slug>[\-\w]+)' +
        '/(?P<suggestion_slug>[\-\w]+)$',
        UploadSuggestionImageView.as_view()
    ),
    url(r'^api/goal/(?P<goal_slug>[\-\w]+)$', GoalView.as_view()),
    url(r'^api/suggestions/(?P<goal_slug>[\-\w]+)$', SuggestionList.as_view()),
    url(
        r'^api/review/(?P<goal_slug>[\-\w]+)/' +
        r'(?P<suggestion_slug>[\-\w]+)$',
        ReviewView.as_view()
    ),
    url(
        r'^api/suggestion/(?P<goal_slug>[\-\w]+)/' +
        r'(?P<suggestion_slug>[\-\w]+)$',
        SuggestionView.as_view()
    ),
    url(
        r'^api/bundle/(?P<goal_slug>[\-\w]+)/' +
        r'(?P<suggestion_slug>[\-\w]+)$',
        BundleView.as_view()
    ),
]

if settings.DEBUG:
    urlpatterns += [
        url(
            r'^media/(?P<path>.*)$',
            static.serve,
            {
                'document_root': settings.MEDIA_ROOT, 'show_indexes': True
            }
        ),
    ]

urlpatterns += [
    url(r'', HomeView.as_view(), name='home'),
]
