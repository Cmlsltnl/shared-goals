import json

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from django.core.urlresolvers import reverse
from django.db import models

from goal.models import GlobalUser, Goal

from suggestion.models import Suggestion

from review.models import Comment, Review

from django.template import loader
from django.shortcuts import get_object_or_404


class Notification(models.Model):
    TEMPLATE_NEW_COMMENT = 0
    TEMPLATE_UPDATED_REVIEW = 1
    TEMPLATE_NEW_REVIEW = 2
    TEMPLATE_NEW_SUGGESTION = 3
    TEMPLATE_CHOICES = (
        (TEMPLATE_NEW_COMMENT, "notification/notify_new_comment.html"),
        (TEMPLATE_UPDATED_REVIEW, "notification/notify_updated_review.html"),
        (TEMPLATE_NEW_REVIEW, "notification/notify_new_review.html"),
        (TEMPLATE_NEW_SUGGESTION, "notification/notify_new_suggestion.html"),
    )

    template = models.PositiveSmallIntegerField(choices=TEMPLATE_CHOICES)
    context = models.TextField()
    is_read = models.BooleanField(default=False)
    owner = models.ForeignKey(GlobalUser, related_name="notifications")
    goal = models.ForeignKey(Goal, related_name="notifications")
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return self.get_template_display()

    @staticmethod
    def create_for_comment(comment):
        n = Notification()
        n.owner = (
            comment.reply_to.owner
            if comment.reply_to else
            comment.review.owner
        )
        n.goal = comment.review.revision.suggestion.goal
        n.template = Notification.TEMPLATE_NEW_COMMENT
        n.context = json.dumps(dict(
            comment_pk=comment.pk,
        ))
        return n

    @staticmethod
    def create_for_review(review):
        n = Notification()
        n.owner = review.revision.suggestion.owner
        n.goal = review.revision.suggestion.goal
        n.template = Notification.TEMPLATE_NEW_REVIEW
        n.context = json.dumps(dict(
            review_pk=review.pk,
        ))
        return n

    @staticmethod
    def create_for_suggestion(suggestion):
        n = Notification()
        n.goal = suggestion.goal
        n.owner = n.goal.owner
        n.template = Notification.TEMPLATE_NEW_SUGGESTION
        n.context = json.dumps(dict(
            suggestion_pk=suggestion.pk,
        ))
        return n

    def html(self):
        t = loader.get_template(self.get_template_display())
        c = json.loads(self.context)

        if self.template == self.TEMPLATE_NEW_COMMENT:
            self.__context_for_new_comment(c)
        if self.template == self.TEMPLATE_UPDATED_REVIEW:
            self.__context_for_new_or_updated_review(c)
        if self.template == self.TEMPLATE_NEW_REVIEW:
            self.__context_for_new_or_updated_review(c)
        if self.template == self.TEMPLATE_NEW_SUGGESTION:
            self.__context_for_new_suggestion(c)

        c['is_read'] = 1 if self.is_read else 0

        parameters = urlencode({'next': c['next_url']})
        c['target_url'] = reverse(
            'follow-notification',
            kwargs=dict(
                notification_id=self.pk
            )) + "?" + parameters
        return t.render(c)

    def __context_for_new_comment(self, c):
        comment = get_object_or_404(Comment, pk=c['comment_pk'])
        c['comment'] = comment

        review = comment.review
        suggestion = review.revision.suggestion
        c['next_url'] = suggestion.get_url() + "#sg-comment-%d" % comment.pk

        if comment.reply_to:
            c['did_what'] = 'replied to your comment'
        else:
            c['did_what'] = 'commented on your review'

    def __context_for_new_or_updated_review(self, c):
        review = get_object_or_404(Review, pk=c['review_pk'])
        suggestion = review.revision.suggestion

        c['review'] = review
        c['suggestion'] = suggestion
        c['next_url'] = suggestion.get_url() + "#sg-review-%d" % review.pk

    def __context_for_new_suggestion(self, c):
        suggestion = get_object_or_404(Suggestion, pk=c['suggestion_pk'])

        c['suggestion'] = suggestion
        c['next_url'] = suggestion.get_url()
