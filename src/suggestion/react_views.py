"""Views for react based presentation."""

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

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
            'image',
            'goal',
            'pk',
            'stars',
        )

    current_revision = RevisionSerializer(
        source='get_current_revision', many=False)


class SuggestionList(APIView):  # noqa
    queryset = Suggestion.objects.all()

    def get(self, request, goal_slug):  # noqa
        queryset = self.queryset.filter(
            is_draft=False, goal__slug=goal_slug
        )
        serializer = SuggestionSerializer(queryset, many=True)
        return Response(serializer.data)
