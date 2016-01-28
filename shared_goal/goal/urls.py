from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.GoalView.as_view(), name='goal'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
]
