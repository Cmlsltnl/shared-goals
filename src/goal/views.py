from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator

from suggestion.models import Suggestion

from notification.models import Notification


def membership_required(view):
    def _wrapper(request, *args, **kw):
        if not request.member:
            return HttpResponseRedirect(
                reverse(
                    'register',
                    kwargs=dict(goal_slug=request.goal.slug)
                )
            )
        return view(request, *args, **kw)
    return _wrapper


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


class GoalView(View):
    def get(self, request, goal_slug):
        suggestions = request.goal.suggestions.filter(
            is_draft=False
        ).order_by('-avg_rating')

        context = {
            'suggestion_lists': chunks(suggestions, 3)
        }
        return render(request, 'goal/goal.html', context)


class GoalsView(View):
    def get(self, request):
        context = {
        }
        return render(request, 'goal/goals.html', context)


class ProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        suggestions = Suggestion.objects.filter(
            owner=request.global_user,
            is_draft=False
        ).order_by('-avg_rating')

        notifications = Notification.objects.filter(
            owner=request.global_user,
            goal=request.goal
        ).order_by('-pub_date')
        context = {
            'suggestion_lists': chunks(suggestions, 3),
            'notifications': notifications
        }
        return render(request, 'goal/profile.html', context)
