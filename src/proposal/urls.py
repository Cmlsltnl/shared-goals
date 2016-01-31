from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^new-proposal/$',
        views.NewProposalView.as_view(),
        name='new-proposal'
    ),
]
