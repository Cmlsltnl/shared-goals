from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.views.generic import View
from django.utils.decorators import method_decorator

from .models import Goal
from .forms import GoalForm

from suggestion.models import Suggestion
from suggestion.utils import apply_cropping_to_image

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
        goals = Goal.objects.filter(
            is_draft=False
        ).order_by('-pub_date')

        context = {
            'goal_lists': chunks(goals, 3)
        }
        return render(request, 'goal/goals.html', context)


class NewGoalView(View):
    def get_posted_form(self, request, goal):
        def is_duplicate_title(title):
            return Goal.objects.filter(
                Q(slug=slugify(title)) & ~Q(pk=goal.pk)
            ).exists()

        form = GoalForm(request.POST, request.FILES)
        form.is_duplicate_title = is_duplicate_title

        return form

    def on_cancel(self):
        return HttpResponseRedirect(reverse('home'))

    def on_save(self, goal):
        return HttpResponseRedirect(
            reverse('goal', kwargs=dict(goal_slug=goal.slug))
        )

    def get_or_create_draft(self, request):
        draft = Goal.objects.filter(
            is_draft=True, owner=request.global_user
        ).first()

        if not draft:
            draft = Goal()
            draft.owner = request.global_user
            draft.save()
        return draft

    def __update_goal_and_save(self, goal, form, submit):
        is_form_valid = form.is_valid()

        if 'title' in form.cleaned_data:
            goal.title = form.cleaned_data['title'] or ''

        if form.cleaned_data.get('image', None):
            goal.image = form.cleaned_data['image']

        if 'cropping' in form.cleaned_data:
            goal.cropping = form.cleaned_data['cropping']

        if is_form_valid and submit == 'save':
            goal.slug = slugify(goal.title)
            apply_cropping_to_image(goal, delete_original=False)
            goal.is_draft = False
            goal.save()
        else:
            goal.save()

        return is_form_valid

    @method_decorator(login_required)
    def get(self, request):
        return self.handle(request)

    @method_decorator(login_required)
    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        goal = self.get_or_create_draft(request)
        is_posting = request.method == 'POST'
        submit = request.POST.get('submit', 'none')

        bound_form = None
        if is_posting:
            bound_form = self.get_posted_form(request, goal)
            should_accept_data = self.__update_goal_and_save(
                goal, bound_form, submit)

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
    def get(self, request):
        suggestions = Suggestion.objects.filter(
            owner=request.global_user,
            is_draft=False
        ).order_by('-avg_rating')

        notifications = Notification.objects.filter(
            owner=request.global_user
        ).order_by('-pub_date')
        context = {
            'suggestion_lists': chunks(suggestions, 3),
            'notifications': notifications
        }
        return render(request, 'goal/profile.html', context)
