from django import forms

from .models import Proposal


class RevisionForm(forms.Form):
    is_duplicate_title = lambda x: False

    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description')

    def clean_title(self):
        if self.is_duplicate_title(self.cleaned_data['title']):
            raise forms.ValidationError(
                "Sorry, this title is already used, please choose another"
            )


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ('image', 'cropping')
