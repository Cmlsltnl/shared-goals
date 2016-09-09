"""Urls."""

from django.conf.urls import include, url

from . import react_views as views


urlpatterns = [
    url(r'^$', views.GoalsView.as_view(), name='home'),
    url(
        r'^to/(?P<goal_slug>[\-\w]+)/$',
        views.GoalView.as_view(),
        name='goal'
    ),
    url(
        r'^to/(?P<goal_slug>[\-\w]+)/profile/(?P<username>[\-\w]+)/$',
        views.ProfileView.as_view(),
        name='profile'
    ),
    url(r'^to/(?P<goal_slug>[\-\w]+)/', include('suggestion.urls')),
]
