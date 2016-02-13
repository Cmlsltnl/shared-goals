from django import forms

from .models import Suggestion


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = ('image', 'cropping', 'type')

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
