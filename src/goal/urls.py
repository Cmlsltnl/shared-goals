from django.conf.urls import include, url

from . import views

urlpatterns = [
    # url(r'^profile/$', views.ProfileView.as_view(), name='global-profile'),
    url(
        r'^to/(?P<goal_slug>[\-\w]+)/profile/(?P<username>[\-\w]+)/$',
        views.ProfileView.as_view(),
        name='profile'
    ),
    url(r'^$', views.GoalsView.as_view(), name='home'),
    url(r'^new-goal$', views.NewGoalView.as_view(), name='new-goal'),
    url(
        r'^to/(?P<goal_slug>[\-\w]+)/join/$',
        views.JoinGoalView.as_view(),
        name='join-goal'
    ),
    url(
        r'^to/(?P<goal_slug>[\-\w]+)/$',
        views.GoalView.as_view(),
        name='goal'
    ),
    url(r'^to/(?P<goal_slug>[\-\w]+)/', include('suggestion.urls')),
    url(r'^to/(?P<goal_slug>[\-\w]+)/', include('review.urls')),
]
