"""Main urls."""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views import static

from goal.react_views import GoalList
from suggestion.react_views import SuggestionList

from react_views import HomeView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/goals', GoalList.as_view()),
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
