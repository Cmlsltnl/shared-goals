"""Views for react based presentation."""

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status

from notification.models import Notification

from goal.models import Member
from review.models import Review
from review.utils import update_rating_and_save

from suggestion.models import Suggestion


class ReviewSerializer(serializers.ModelSerializer):  # noqa
    class Meta:  # noqa
        model = Review

    def update(self, instance, validated_data):  # noqa
        instance.rating = validated_data['rating']
        instance.experience = validated_data['experience']
        instance.description = validated_data['description']
        instance.save()
        return instance


class ReviewView(APIView):  # noqa
    queryset = Review.objects.all()

    def _get_data(self, request, goal_slug, suggestion_slug):
        self.member = Member.lookup(request.user, goal_slug)
        if self.member:
            self.suggestion = get_object_or_404(
                Suggestion,
                slug=suggestion_slug,
                goal__slug=goal_slug
            )

            self.review = Review.objects.filter(
                revision__suggestion=self.suggestion,
                owner=self.member.global_user
            ).first()

    def _create_review(self):
        self.review = Review()
        self.review.owner = self.member.global_user
        self.review.revision = self.suggestion.get_current_revision()
        self.review.save()

    def get(self, request, goal_slug, suggestion_slug):  # noqa
        self._get_data(request, goal_slug, suggestion_slug)
        if not self.review:
            self._create_review()
        serializer = ReviewSerializer(self.review)
        return Response(serializer.data)

    def post(self, request, goal_slug, suggestion_slug):  # noqa
        self._get_data(request, goal_slug, suggestion_slug)
        if not self.review:
            self._create_review()

        data = ReviewSerializer(self.review).data
        data.update(request.data)

        serializer = ReviewSerializer(instance=self.review, data=data)
        if serializer.is_valid():
            self.review = serializer.save(is_draft=False)
            update_rating_and_save(self.review.revision.suggestion)
            self.review.comments.filter(is_draft=False).delete()
            notification = Notification.create_for_review(self.review)
            if notification.owner != self.review.owner:
                notification.save()
            return Response(
                {'success': 1},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'success': 0,
                    'errors': serializer.errors
                },
                status=status.HTTP_200_OK
            )
