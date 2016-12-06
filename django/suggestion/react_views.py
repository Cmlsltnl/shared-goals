"""Views for react based presentation."""

import json

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status

from suggestion.models import Suggestion, Revision
from goal.react_views import GlobalUserSerializer
from goal.models import Goal, Member
from goal.utils import singlify


class RevisionSerializer(serializers.ModelSerializer):  # noqa
    class Meta:  # noqa
        model = Revision
        fields = ('title', 'description', 'pub_date_display')


class SuggestionUpdateSerializer(serializers.Serializer):  # noqa
    type = serializers.IntegerField()
    description = serializers.CharField(max_length=200)
    title = serializers.CharField(max_length=100)
    is_draft = serializers.BooleanField()

    def validate_title(self, value):  # noqa
        """
        Check that the blog post is about Django.
        """
        this_pk = self.instance.pk if self.instance else -1
        if Suggestion.objects.filter(
            Q(slug=slugify(value)) & ~Q(pk=this_pk)
        ).exists():
            raise serializers.ValidationError(
                "This title is already in use, please choose a different one"
            )
        return value

    def update(self, instance, validated_data):  # noqa
        revision = (
            instance.get_current_revision()
            if validated_data['is_draft']
            else Revision()
        )
        revision.title = validated_data['title']
        revision.description = validated_data['description']
        revision.suggestion = instance
        revision.save()

        instance.type = validated_data['type']
        instance.is_draft = validated_data['is_draft']
        instance.slug = slugify(validated_data['title'])
        instance.save()

        return instance


class SuggestionSerializer(serializers.ModelSerializer):  # noqa
    class Meta:  # noqa
        model = Suggestion
        fields = '__all__'

    current_revision = RevisionSerializer(
        source='get_current_revision', many=False)

    type_display = serializers.CharField(
        source='get_type_display', max_length=200)

    owner = GlobalUserSerializer(many=False)

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
        serializer = SuggestionSerializer(queryset, many=False)
        return Response(serializer.data)


class SuggestionBaseView(APIView):  # noqa
    queryset = Suggestion.objects.all()

    bad_request = Response(
        {}, status=status.HTTP_400_BAD_REQUEST
    )

    def _get_data(self, request, goal_slug, suggestion_slug=None):
        self.member = Member.lookup(request.user, goal_slug)
        if self.member:
            self.goal = get_object_or_404(
                Goal,
                slug=goal_slug
            )
            if suggestion_slug:
                self.suggestion = get_object_or_404(
                    Suggestion,
                    slug=suggestion_slug
                )
            else:
                self.suggestion = self.queryset.filter(
                    is_draft=True,
                    owner=self.member.global_user,
                    goal__slug=goal_slug
                ).first()

    def _create_draft_suggestion(self):
        suggestion = Suggestion()
        suggestion.owner = self.member.global_user
        suggestion.goal = self.goal
        suggestion.is_draft = True
        suggestion.save()

        revision = Revision()
        revision.title = "not set"
        revision.description = "not set"
        revision.suggestion = suggestion
        revision.save()

        return suggestion

class UploadSuggestionImageView(SuggestionBaseView):  # noqa
    queryset = Suggestion.objects.all()

    bad_request = Response(
        {}, status=status.HTTP_400_BAD_REQUEST
    )

    def post(self, request, goal_slug, suggestion_slug=None):  # noqa
        if request.user.is_anonymous():
            return self.bad_request

        self._get_data(request, goal_slug, suggestion_slug)
        if not self.member:
            return self.bad_request

        if not suggestion_slug and not self.suggestion:
            self.suggestion = self._create_draft_suggestion()

        if "image" not in request.data:
            return self.bad_request

        img = request.data['image']
        self.suggestion.uncropped_image = (
            default_storage.save(
                'suggestions/' + img.name, ContentFile(img.read())
            )
        )
        self.suggestion.save()

        return Response(
            {
                'success': 1,
                'image_url': self.suggestion.uncropped_image.url
            },
            status=status.HTTP_200_OK
        )


class EditSuggestionView(SuggestionBaseView):  # noqa
    def get(self, request, goal_slug, suggestion_slug=None):  # noqa
        if request.user.is_anonymous():
            return self.bad_request

        self._get_data(request, goal_slug, suggestion_slug)
        if not self.member:
            return self.bad_request

        if not suggestion_slug and not self.suggestion:
            self.suggestion = self._create_draft_suggestion()
        serializer = SuggestionSerializer(self.suggestion)
        return Response(serializer.data)


    def post(self, request, goal_slug, suggestion_slug=None):  # noqa
        if request.user.is_anonymous():
            return self.bad_request

        self._get_data(request, goal_slug, suggestion_slug)
        if not self.member:
            return self.bad_request

        if not self.suggestion:
            self.suggestion = self._create_draft_suggestion()

        data = singlify(request.data)
        serializer = SuggestionUpdateSerializer(
            instance=self.suggestion, data=data
        )
        if serializer.is_valid():
            self.suggestion = serializer.save()
            if (
                self.suggestion.uncropped_image and
                'crop' in request.data and
                not serializer.validated_data['is_draft']
            ):
                crop = json.loads(request.data['crop'])
                self.suggestion.apply_cropping(crop)

            return Response(
                {
                    'success': 1,
                    'suggestion_slug': self.suggestion.slug
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
