import json

from django import forms
from django.db.models import Q
from django.template.defaultfilters import slugify

from .models import Suggestion, Revision

from goal.utils import apply_cropping_to_image

from notification.models import Notification


class SuggestionForm(forms.ModelForm):
    cropped_image_key = "cropped_suggestion_image"

    class Meta:
        model = Suggestion
        fields = ('image', 'type')

    is_duplicate_title = lambda x: False

    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description')

    def clean_title(self):
        data = self.cleaned_data['title']
        if self.is_duplicate_title(data):
            raise forms.ValidationError(
                "Sorry, this title is already used, please choose another"
            )
        return data

    @staticmethod
    def get_posted_form(request, suggestion):
        def is_duplicate_title(title):
            return suggestion.goal.suggestions.filter(
                Q(slug=slugify(title)) & ~Q(pk=suggestion.pk)
            ).exists()

        form = SuggestionForm(request.POST, request.FILES)
        form.is_duplicate_title = is_duplicate_title
        form.cropping = (
            json.loads(request.POST[SuggestionForm.cropped_image_key])
            if SuggestionForm.cropped_image_key in request.POST else
            None
        )

        return form

    @staticmethod
    def get_populated_form(request, suggestion):
        return SuggestionForm(
            instance=suggestion,
            initial=suggestion.get_current_revision().__dict__
        )

    @staticmethod
    def get_or_create_draft(goal, global_user):
        draft = Suggestion.objects.filter(
            is_draft=True, owner=global_user
        ).first()

        if not draft:
            draft = Suggestion()
            draft.owner = global_user
            draft.goal = goal
            draft.save()

            revision = Revision()
            revision.suggestion = draft
            revision.save()
        return draft

    def update_suggestion_and_save(self, suggestion, submit):
        is_form_valid = self.is_valid()

        current_revision = suggestion.get_current_revision()
        if 'title' in self.cleaned_data:
            current_revision.title = self.cleaned_data['title'] or ''
        if 'description' in self.cleaned_data:
            current_revision.description = \
                self.cleaned_data['description'] or ''
        current_revision.save()

        suggestion.type = self.cleaned_data['type']
        if self.cleaned_data.get('image', None):
            suggestion.image = self.cleaned_data['image']

        if is_form_valid and submit == 'save':
            sx = (
                float(self.cropping['natural_width']) /
                float(self.cropping['display_width'])
            )
            sy = (
                float(self.cropping['natural_height']) /
                float(self.cropping['display_height'])
            )
            apply_cropping_to_image(
                suggestion.image,
                self.cropping['x'] * sx,
                self.cropping['y'] * sy,
                self.cropping['w'] * sx,
                self.cropping['h'] * sy,
            )

            suggestion.slug = slugify(
                suggestion.get_current_revision().title)
            suggestion.is_draft = False
            suggestion.save()

            notification = Notification.create_for_suggestion(suggestion)
            if notification.owner != suggestion.owner:
                notification.save()

        else:
            suggestion.save()

        return is_form_valid

    def create_new_revision(self, suggestion):
        is_form_valid = self.is_valid()

        if is_form_valid:
            revision = Revision()
            revision.title = self.cleaned_data['title']
            revision.description = self.cleaned_data['description']
            revision.suggestion = suggestion
            revision.save()

        return is_form_valid
