from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from django.utils.decorators import method_decorator

from .models import Member, GlobalUser, Goal
from .forms import GoalForm

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


class GoalView(View):
    def get(self, request, goal_slug):
        suggestions = request.goal.suggestions.filter(
            is_draft=False
        ).order_by('-avg_rating')

        context = {
            'suggestions': suggestions,
        }
        return render(request, 'goal/goal.html', context)


class MembersView(View):
    def get(self, request, goal_slug):
        members = request.goal.members.all()

        context = {
            'members': members,
        }
        return render(request, 'goal/members.html', context)


class GoalsView(View):
    def get(self, request):
        goals = Goal.objects.filter(
            is_draft=False
        ).order_by('-pub_date')

        context = {
            'goals': goals
        }
        return render(request, 'goal/goals.html', context)


class JoinGoalView(View):
    @method_decorator(login_required)
    def get(self, request, goal_slug):
        Member.objects.get_or_create(
            global_user=request.global_user,
            goal=request.goal
        )
        return HttpResponseRedirect(
            reverse('goal', kwargs=dict(goal_slug=request.goal.slug))
        )


class NewGoalView(View):
    def on_cancel(self):
        return HttpResponseRedirect(reverse('home'))

    def on_save(self, goal):
        return HttpResponseRedirect(
            reverse('goal', kwargs=dict(goal_slug=goal.slug))
        )

    @method_decorator(login_required)
    def get(self, request):
        return self.handle(request)

    @method_decorator(login_required)
    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        goal = GoalForm.get_or_create_draft(request)
        is_posting = request.method == 'POST'
        submit = request.POST.get('submit', 'none')

        bound_form = None
        if is_posting:
            bound_form = GoalForm.get_posted_form(request, goal)
            should_accept_data = bound_form.update_goal_and_save(
                goal, submit)

            if should_accept_data and submit == 'save':
                return self.on_save(goal)
            elif submit == 'cancel':
                return self.on_cancel()

        form = (
            bound_form
            if is_posting and submit == 'save' else
            GoalForm(instance=goal)
        )

        context = {
            'form': form,
            'crop_settings': {
                'url': goal.image.url if goal.image else "",
                'klass': 'goal--image crop-image',
                'output_key': form.cropped_image_key,
                'jcrop': dict(
                    aspectRatio=360.0 / 200.0,
                    setSelect=[0, 0, 10000, 10000],
                ),
            },
            'show_image_form': True,
            'show_errors': submit == 'save',
            'post_button_label': 'Submit',
            'submit_button_header': (
                'All done, press Submit to publish your goal'
            ),
            'show_delete_button': False
        }

        return render(request, 'goal/edit_goal.html', context)


class ProfileView(View):
    @method_decorator(login_required)
    def get(self, request, goal_slug, username):
        global_user = get_object_or_404(
            GlobalUser,
            user__username=username
        )
        suggestions = Suggestion.objects.filter(
            owner=request.global_user,
            is_draft=False
        ).order_by('-avg_rating')

        if request.goal:
            suggestions = suggestions.filter(goal=request.goal)

        notifications = Notification.objects.filter(
            owner=request.global_user
        ).order_by('-pub_date')
        context = {
            'suggestions': suggestions,
            'notifications': notifications,
            'global_user': global_user,
            'show_notifications': request.global_user == global_user,
        }
        return render(request, 'goal/profile.html', context)
