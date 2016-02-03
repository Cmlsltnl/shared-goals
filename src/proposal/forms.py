from django import forms
from image_cropping import ImageCropWidget
from .models import Proposal


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
