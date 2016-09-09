"""Views for react based presentation."""

from django.shortcuts import get_object_or_404, render
from django.views.generic import View

from rest_framework import serializers, viewsets

from suggestion.models import Suggestion, Revision


class RevisionSerializer(serializers.ModelSerializer):  # noqa
    class Meta:  # noqa
        model = Revision
        fields = ('title',)


class SuggestionSerializer(serializers.ModelSerializer):  # noqa
    class Meta:  # noqa
        model = Suggestion
        fields = (
            'current_revision',
            'get_type_display',
            'get_url',
            'image',
            'goal',
            'pk',
            'stars',
        )

    current_revision = RevisionSerializer(
        source='get_current_revision', many=False)


class SuggestionViewSet(viewsets.ModelViewSet):  # noqa
    queryset = Suggestion.objects.filter(is_draft=False)
    serializer_class = SuggestionSerializer
    filter_fields = ('goal',)


class SuggestionView(View):  # noqa
    def get(self, request, goal_slug, suggestion_slug):  # noqa
        suggestion = get_object_or_404(Suggestion, slug=suggestion_slug)
        revision = suggestion.get_current_revision()

        context = {
            'suggestion': suggestion,
            'revision': revision,
        }
        return render(request, 'react_suggestion/suggestion.html', context)
