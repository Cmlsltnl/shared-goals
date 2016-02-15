from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^ajax-notification-read/(?P<notification_id>\d+)/$',
        views.NotificationReadView.as_view(),
        name='notification-read'
    ),
]
