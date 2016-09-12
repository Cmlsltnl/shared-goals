"""Views for react based presentation."""

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Goal


class GoalSerializer(serializers.ModelSerializer):  # noqa
    class Meta:  # noqa
        model = Goal
        fields = ('title', 'pk')


class GoalList(APIView):  # noqa
    queryset = Goal.objects.all()

    def get(self, request):  # noqa
        serializer = GoalSerializer(
            self.queryset.filter(is_draft=False),
            many=True
        )
        return Response(serializer.data)
