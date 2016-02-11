from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^new-suggestion/$',
        views.EditSuggestionView.as_view(),
        name='new-suggestion'
    ),
    url(
        r'^edit-suggestion/(?P<suggestion_slug>[\-\w]+)/$',
        views.EditSuggestionView.as_view(),
        name='edit-suggestion'
    ),
    url(
        r'^by/(?P<suggestion_slug>[\-\w]+)/$',
        views.SuggestionView.as_view(),
        name='suggestion'
    ),
    url(
        r'^by/(?P<suggestion_slug>[\-\w]+)/revision/(?P<revision_pk>[\d]+)$',
        views.RevisionView.as_view(),
        name='revision'
    ),
]
