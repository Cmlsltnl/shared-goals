import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator

from notification.models import Notification


class NotificationReadView(View):

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(NotificationReadView, self).dispatch(*args, **kwargs)

    def post(self, request, notification_id):
        notification = get_object_or_404(
            Notification,
            owner=request.global_user,
            pk=notification_id
        )

        notification.is_read = True
        notification.save()

        return HttpResponse(
            json.dumps({
                'success': True,
            }),
            content_type="application/json"
        )
