from django import forms

from .models import Comment, Proposal, Review


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


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'description')

    def clean_rating(self):
        data = self.cleaned_data['rating']
        if not data >= 1 and data <= 5:
            raise forms.ValidationError("Please choose a rating")
        return data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
