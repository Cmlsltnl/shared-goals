import json

from django import forms
from django.db.models import Q
from django.template.defaultfilters import slugify

from .models import Goal
from .utils import apply_cropping_to_image


class GoalForm(forms.ModelForm):
    cropped_image_key = "cropped_goal_image"

    class Meta:
        model = Goal
        fields = ('title', 'image')

    is_duplicate_title = lambda x: False

    def clean_title(self):
        data = self.cleaned_data['title']
        if self.is_duplicate_title(data):
            raise forms.ValidationError(
                "Sorry, this title is already used, please choose another"
            )
        return data

    @staticmethod
    def get_posted_form(request, goal):
        def is_duplicate_title(title):
            return Goal.objects.filter(
                Q(slug=slugify(title)) & ~Q(pk=goal.pk)
            ).exists()

        form = GoalForm(request.POST, request.FILES)
        form.is_duplicate_title = is_duplicate_title
        form.cropping = (
            json.loads(request.POST[GoalForm.cropped_image_key])
            if GoalForm.cropped_image_key in request.POST else
            None
        )

        return form

    @staticmethod
    def get_or_create_draft(request):
        draft = Goal.objects.filter(
            is_draft=True, owner=request.global_user
        ).first()

        if not draft:
            draft = Goal()
            draft.owner = request.global_user
            draft.save()
        return draft

    def update_goal_and_save(self, goal, submit):
        is_form_valid = self.is_valid()

        if 'title' in self.cleaned_data:
            goal.title = self.cleaned_data['title'] or ''

        if self.cleaned_data.get('image', None):
            goal.image = self.cleaned_data['image']

        if is_form_valid and submit == 'save':
            goal.slug = slugify(goal.title)
            sx = (
                float(self.cropping['natural_width']) /
                float(self.cropping['display_width'])
            )
            sy = (
                float(self.cropping['natural_height']) /
                float(self.cropping['display_height'])
            )
            apply_cropping_to_image(
                goal.image,
                self.cropping['x'] * sx,
                self.cropping['y'] * sy,
                self.cropping['w'] * sx,
                self.cropping['h'] * sy,
            )
            goal.is_draft = False
            goal.save()
        else:
            goal.save()

        return is_form_valid
