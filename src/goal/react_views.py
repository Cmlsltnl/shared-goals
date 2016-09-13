"""Views for react based presentation."""

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import GlobalUser, Goal


class GoalSerializer(serializers.ModelSerializer):  # noqa
    class Meta:  # noqa
        model = Goal
        fields = ('title', 'pk')


class GlobalUserSerializer(serializers.ModelSerializer):  # noqa
    class Meta:  # noqa
        model = GlobalUser
        fields = ('name', 'pk')


class GoalListView(APIView):  # noqa
    queryset = Goal.objects.all()

    def get(self, request):  # noqa
        serializer = GoalSerializer(
            self.queryset.filter(is_draft=False),
            many=True
        )
        return Response(serializer.data)


class GoalView(APIView):  # noqa
    queryset = Goal.objects.all()

    def get(self, request, goal_slug):  # noqa
        serializer = GoalSerializer(
            self.queryset.get(slug=goal_slug),
            many=False
        )
        return Response(serializer.data)
