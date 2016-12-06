from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^follow/(?P<notification_id>\d+)/$',
        views.NotificationFollowView.as_view(),
        name='follow-notification'
    ),
]
