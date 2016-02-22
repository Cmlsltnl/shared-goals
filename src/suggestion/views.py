from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from django.utils.decorators import method_decorator

from goal.views import membership_required

from suggestion.forms import SuggestionForm
from suggestion.models import Suggestion, Revision


class PostSuggestionView(View):
    def on_cancel(self, goal_slug):
        # todo redirect to previous page
        return HttpResponseRedirect(
            reverse('goal', kwargs=dict(goal_slug=goal_slug))
        )

    def on_save(self, goal_slug, suggestion_slug):
        return HttpResponseRedirect(
            reverse(
                'suggestion',
                kwargs=dict(
                    goal_slug=goal_slug,
                    suggestion_slug=suggestion_slug
                )
            )
        )


class NewSuggestionView(PostSuggestionView):

    @method_decorator(membership_required)
    @method_decorator(login_required)
    def get(self, request, goal_slug):
        return self.handle(request, goal_slug)

    @method_decorator(membership_required)
    @method_decorator(login_required)
    def post(self, request, goal_slug):
        return self.handle(request, goal_slug)

    def handle(self, request, goal_slug):
        suggestion = SuggestionForm.get_or_create_draft(
            request.goal, request.global_user)
        is_posting = request.method == 'POST'
        submit = request.POST.get('submit', 'none')

        bound_form = None
        if is_posting:
            bound_form = SuggestionForm.get_posted_form(request, suggestion)
            should_accept_data = bound_form.update_suggestion_and_save(
                suggestion, submit)

            if should_accept_data and submit == 'save':
                return self.on_save(request.goal.slug, suggestion.slug)
            elif submit == 'cancel':
                return self.on_cancel(request.goal.slug)

        if is_posting and submit == 'save':
            form = bound_form
        else:
            form = SuggestionForm.get_populated_form(request, suggestion)

        context = {
            'form': form,
            'crop_settings': {
                'url': suggestion.image.url if suggestion.image else "",
                'klass': 'suggestion--image crop-image',
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
                'All done, press Submit to publish your suggestion'
            ),
            'show_delete_button': False
        }

        return render(request, 'suggestion/edit_suggestion.html', context)


class UpdateSuggestionView(PostSuggestionView):

    @method_decorator(membership_required)
    @method_decorator(login_required)
    def get(self, request, goal_slug, suggestion_slug):
        return self.handle(request, goal_slug, suggestion_slug)

    @method_decorator(membership_required)
    @method_decorator(login_required)
    def post(self, request, goal_slug, suggestion_slug):
        return self.handle(request, goal_slug, suggestion_slug)

    def handle(self, request, goal_slug, suggestion_slug):
        suggestion = get_object_or_404(Suggestion, slug=suggestion_slug)
        is_posting = request.method == 'POST'
        submit = request.POST.get('submit', 'none')

        bound_form = None
        if is_posting:
            if submit == 'cancel':
                return self.on_cancel(request.goal.slug)
            if submit == 'delete':
                suggestion.delete()
                return self.on_cancel(request.goal.slug)

            bound_form = SuggestionForm.get_posted_form(request, suggestion)
            if bound_form.create_new_revision(suggestion):
                return self.on_save(request.goal.slug, suggestion.slug)

        form = (
            bound_form
            if is_posting else
            SuggestionForm.get_populated_form(request, suggestion)
        )

        context = {
            'form': form,
            'show_image_form': False,
            'show_errors': True,
            'post_button_label': "Update",
            'submit_button_header': 'Press Update to publish your changes',
            'show_delete_button': True,
        }

        return render(request, 'suggestion/edit_suggestion.html', context)


class SuggestionView(View):
    def get(self, request, goal_slug, suggestion_slug):
        suggestion = get_object_or_404(Suggestion, slug=suggestion_slug)
        revision = suggestion.get_current_revision()

        context = {
            'suggestion': suggestion,
            'revision': revision,
        }
        return render(request, 'suggestion/suggestion.html', context)


class RevisionView(View):
    def get(self, request, goal_slug, suggestion_slug, revision_pk):
        revision = get_object_or_404(Revision, pk=revision_pk)

        context = {
            'suggestion': revision.suggestion,
            'revision': revision,
        }
        return render(request, 'suggestion/revision.html', context)
