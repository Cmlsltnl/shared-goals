from django import forms

from .models import Comment, Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'experience', 'description')

    def clean_rating(self):
        data = self.cleaned_data['rating']
        if not data >= 1 and data <= 5:
            raise forms.ValidationError("Please choose a rating")
        return data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
