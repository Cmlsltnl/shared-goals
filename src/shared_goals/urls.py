from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^to/(?P<goal_slug>[\-\w]+)/', include('goal.urls')),
    url(r'^to/(?P<goal_slug>[\-\w]+)/', include('suggestion.urls')),
    url(r'^to/(?P<goal_slug>[\-\w]+)/', include('review.urls')),
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
