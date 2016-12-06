from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.utils.decorators import method_decorator

from notification.models import Notification


class NotificationFollowView(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NotificationFollowView, self).dispatch(*args, **kwargs)

    def get(self, request, notification_id):
        notification = get_object_or_404(
            Notification,
            owner=request.global_user,
            pk=notification_id
        )

        notification.is_read = True
        notification.save()
        return HttpResponseRedirect(request.GET['next'])
