"""Views for react based presentation."""

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from suggestion.models import Suggestion, Revision
from goal.react_views import GlobalUserSerializer


class RevisionSerializer(serializers.ModelSerializer):  # noqa
    class Meta:  # noqa
        model = Revision
        fields = ('title', 'description', 'pub_date')


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
            'owner',
        )

    current_revision = RevisionSerializer(
        source='get_current_revision', many=False)

    owner = GlobalUserSerializer(many=False)


class SuggestionExtSerializer(SuggestionSerializer):  # noqa
    class Meta(SuggestionSerializer.Meta):  # noqa
        depth = 1


class SuggestionList(APIView):  # noqa
    queryset = Suggestion.objects.all()

    def get(self, request, goal_slug):  # noqa
        queryset = self.queryset.filter(
            is_draft=False, goal__slug=goal_slug
        )
        serializer = SuggestionSerializer(queryset, many=True)
        return Response(serializer.data)


class SuggestionView(APIView):  # noqa
    queryset = Suggestion.objects.all()

    def get(self, request, goal_slug, suggestion_slug):  # noqa
        queryset = self.queryset.get(
            is_draft=False, goal__slug=goal_slug, slug=suggestion_slug
        )
        serializer = SuggestionExtSerializer(queryset, many=False)
        return Response(serializer.data)
