from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^$', views.GoalsView.as_view(), name='home'),
    url(
        r'^to/(?P<goal_slug>[\-\w]+)/$',
        views.GoalView.as_view(),
        name='goal'
    ),
    url(r'^to/(?P<goal_slug>[\-\w]+)/', include('suggestion.urls')),
    url(r'^to/(?P<goal_slug>[\-\w]+)/', include('review.urls')),
]
