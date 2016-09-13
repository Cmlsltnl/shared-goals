"""Main urls."""

from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.views import static

from goal.react_views import GoalListView, GoalView
from suggestion.react_views import SuggestionList

from react_views import HomeView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/goals$', GoalListView.as_view()),
    url(r'^api/goal/(?P<goal_slug>[\-\w]+)$', GoalView.as_view()),
    url(r'^api/suggestions/(?P<goal_slug>[\-\w]+)$', SuggestionList.as_view()),
    url(r'', HomeView.as_view(), name='home'),
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
