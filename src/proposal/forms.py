from django import forms
from image_cropping import ImageCropWidget
from .models import Proposal, Review


class ProposalForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100)
    description = forms.CharField(label='Description')


class ProposalImageForm(forms.ModelForm):
    class Meta:
        widgets = {
            'image': ImageCropWidget,
        }

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
