"""React urls for suggestions."""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^by/(?P<suggestion_slug>[\-\w]+)/$',
        views.SuggestionView.as_view(),
        name='suggestion'
    ),
]
