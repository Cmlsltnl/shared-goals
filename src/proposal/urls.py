from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^new-proposal/$',
        views.EditProposalView.as_view(),
        name='new-proposal'
    ),
    url(
        r'^edit-proposal/(?P<proposal_slug>[\-\w]+)/$',
        views.EditProposalView.as_view(),
        name='edit-proposal'
    ),
    url(
        r'^by/(?P<proposal_slug>[\-\w]+)/$',
        views.ProposalView.as_view(),
        name='proposal'
    ),
    url(
        r'^by/(?P<proposal_slug>[\-\w]+)/revision/(?P<revision_pk>[\d]+)$',
        views.RevisionView.as_view(),
        name='revision'
    ),
]
