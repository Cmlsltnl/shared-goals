from django import forms

from .models import Goal


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ('title', 'image', 'cropping')

    is_duplicate_title = lambda x: False

    def clean_title(self):
        data = self.cleaned_data['title']
        if self.is_duplicate_title(data):
            raise forms.ValidationError(
                "Sorry, this title is already used, please choose another"
            )
        return data
