from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^goal/', include('goal.urls')),
    url(r'^admin/', admin.site.urls),
]
