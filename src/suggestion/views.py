from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.template.defaultfilters import slugify
from django.views.generic import View
from django.utils.decorators import method_decorator

from goal.views import membership_required

from suggestion.forms import RevisionForm, SuggestionForm
from suggestion.models import Suggestion, Revision


class EditSuggestionView(View):
    def __get_or_create_draft(self, request):
        draft = Suggestion.objects.filter(
            is_draft=True, owner=request.member
        ).first()

        if not draft:
            draft = Suggestion()
            draft.owner = request.member
            draft.goal = request.goal
            draft.save()

            revision = Revision()
            revision.suggestion = draft
            revision.save()
        return draft

    def __get_posted_forms(self, request, suggestion):
        def is_duplicate_title(title):
            return suggestion.goal.suggestions.filter(
                Q(slug=slugify(title)) & ~Q(pk=suggestion.pk)
            ).exists()

        revision_form = RevisionForm(request.POST, request.FILES)
        revision_form.is_duplicate_title = is_duplicate_title

        return (revision_form, SuggestionForm(request.POST, request.FILES))

    def __get_populated_forms(self, request, suggestion):
        suggestion_form = SuggestionForm(
            initial=suggestion.__dict__,
            files=dict(image=suggestion.image)
        )
        return (
            RevisionForm(initial=suggestion.get_current_revision().__dict__),
            suggestion_form
        )

    def __update_suggestion_and_save(self, suggestion, request):
        revision_form, suggestion_form = \
            self.__get_posted_forms(request, suggestion)
        is_revision_form_valid = revision_form.is_valid()
        is_suggestion_form_valid = suggestion_form.is_valid()

        current_revision = suggestion.get_current_revision()
        current_revision.title = revision_form['title'].value()
        current_revision.description = revision_form['description'].value()
        current_revision.save()

        if is_suggestion_form_valid:
            if 'image' in request.FILES:
                suggestion.image = suggestion_form.cleaned_data['image']
            suggestion.cropping = suggestion_form.cleaned_data['cropping']

            if is_revision_form_valid and request.POST['submit'] == 'save':
                suggestion.slug = slugify(
                    suggestion.get_current_revision().title)
                suggestion.apply_cropping_to_image(replace_original=True)
                suggestion.is_draft = False

            suggestion.save()

        return is_revision_form_valid and is_suggestion_form_valid

    def __create_new_revision(self, suggestion, request):
        revision_form, _ = self.__get_posted_forms(request, suggestion)

        is_revision_form_valid = revision_form.is_valid()
        if is_revision_form_valid:
            revision = Revision()
            revision.title = revision_form['title'].value()
            revision.description = revision_form['description'].value()
            revision.suggestion = suggestion
            revision.save()

        return is_revision_form_valid

    def __on_cancel(self, goal_slug):
        # todo redirect to previous page
        return HttpResponseRedirect(
            reverse(
                'goal',
                kwargs=dict(
                    goal_slug=goal_slug
                )
            )
        )

    def __on_save(self, goal_slug, suggestion_slug):
        return HttpResponseRedirect(
            reverse(
                'suggestion',
                kwargs=dict(
                    goal_slug=goal_slug,
                    suggestion_slug=suggestion_slug
                )
            )
        )

    @method_decorator(membership_required)
    @method_decorator(login_required)
    def get(self, request, goal_slug, suggestion_slug=""):
        return self.handle(request, goal_slug, suggestion_slug)

    @method_decorator(membership_required)
    @method_decorator(login_required)
    def post(self, request, goal_slug, suggestion_slug=""):
        return self.handle(request, goal_slug, suggestion_slug)

    def handle(self, request, goal_slug, suggestion_slug):
        suggestion = (
            get_object_or_404(Suggestion, slug=suggestion_slug)
            if suggestion_slug else
            self.__get_or_create_draft(request)
        )
        is_posting = request.method == 'POST'

        if is_posting:
            if suggestion_slug:
                should_accept_data = request.POST['submit'] == 'cancel' or \
                    self.__create_new_revision(suggestion, request)
            else:
                should_accept_data = \
                    self.__update_suggestion_and_save(suggestion, request)

            if request.POST['submit'] == 'cancel':
                return self.__on_cancel(request.goal.slug)
            elif request.POST['submit'] == 'save' and should_accept_data:
                return self.__on_save(request.goal.slug, suggestion.slug)

        revision_form, suggestion_form = (
            self.__get_posted_forms(request, suggestion)
            if is_posting and request.POST['submit'] == 'save' else
            self.__get_populated_forms(request, suggestion)
        )

        context = {
            'revision_form': revision_form,
            'suggestion_form': (
                suggestion_form if suggestion.is_draft else None
            ),
            'cancel_button_label':
                "Save draft" if suggestion.is_draft else "Cancel",
            'post_button_label':
                "Submit" if suggestion.is_draft else "Update",
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
