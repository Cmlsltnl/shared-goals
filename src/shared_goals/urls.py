from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^(?P<goal_slug>[\-\w]+)/', include('goal.urls')),
]
