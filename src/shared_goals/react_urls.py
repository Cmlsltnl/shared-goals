"""Main urls."""

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views import static

from rest_framework import routers

from goal.react_views import GoalViewSet
from suggestion.react_views import SuggestionViewSet


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'goals', GoalViewSet)
router.register(r'suggestions', SuggestionViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(
        r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    ),
    url(r'', include('goal.react_urls')),
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
