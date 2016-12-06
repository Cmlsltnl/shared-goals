"""Views for react based presentation."""

from django.db.models import Q
from django.template.defaultfilters import slugify

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import GlobalUser, Goal


class GoalSerializer(serializers.ModelSerializer):  # noqa
    class Meta:  # noqa
        model = Goal
        fields = ('title', 'id', 'slug')

    def validate_title(self, value):  # noqa
        """
        Check that the blog post is about Django.
        """
        this_pk = self.instance.pk if self.instance else -1
        if Goal.objects.filter(
            Q(slug=slugify(value)) & ~Q(pk=this_pk)
        ).exists():
            raise serializers.ValidationError(
                "This title is already in use, please choose a different one"
            )
        return value

    def create(self, validated_data):  # noqa
        data = dict(validated_data)
        data["slug"] = slugify(data["title"])
        return Goal.objects.create(**data)


class GlobalUserSerializer(serializers.ModelSerializer):  # noqa
    class Meta:  # noqa
        model = GlobalUser
        fields = ('name', 'id')


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


class NewGoalView(APIView):  # noqa
    queryset = Goal.objects.all()

    def post(self, request):  # noqa
        if request.user.is_anonymous():
            return Response(
                {}, status=status.HTTP_400_BAD_REQUEST
            )

        data = dict(request.POST)
        data.update(dict(
            owner=request.user.global_user,
            is_draft=False,
            title=request.POST.get('title'),
        ))

        serializer = GoalSerializer(data=data)
        if serializer.is_valid():
            goal = serializer.save()
            return Response(
                {
                    'success': 1,
                    'goal_slug': goal.slug
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'success': 0,
                    'errors': serializer.errors
                },
                status=status.HTTP_200_OK
            )
