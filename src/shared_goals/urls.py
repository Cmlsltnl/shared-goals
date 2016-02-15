from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^notification/', include('notification.urls')),
    url(r'', include('goal.urls')),
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
