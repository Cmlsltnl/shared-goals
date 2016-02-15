import json

from django.core.urlresolvers import reverse
from django.db import models

from goal.models import GlobalUser, Goal

from review.models import Comment

from django.template import loader
from django.shortcuts import get_object_or_404


class Notification(models.Model):
    TEMPLATE_NEW_COMMENT = 0
    TEMPLATE_NEW_REVIEW = 1
    TEMPLATE_NEW_SUGGESTION = 2
    TEMPLATE_CHOICES = (
        (TEMPLATE_NEW_COMMENT, "notification/notify_new_comment.html"),
        (TEMPLATE_NEW_REVIEW, "notification/notify_new_review.html"),
        (TEMPLATE_NEW_SUGGESTION, "notification/notify_new_suggestion.html"),
    )

    template = models.PositiveSmallIntegerField(choices=TEMPLATE_CHOICES)
    context = models.TextField()
    is_read = models.BooleanField(default=False)
    owner = models.ForeignKey(GlobalUser, related_name="notifications")
    goal = models.ForeignKey(Goal, related_name="notifications")

    def __str__(self):
        return self.get_template_display()

    @staticmethod
    def create_for_comment(comment):
        n = Notification()
        n.owner = comment.reply_to.owner
        n.goal = comment.review.revision.suggestion.goal
        n.template = Notification.TEMPLATE_NEW_COMMENT
        n.context = json.dumps(dict(
            comment_pk=comment.pk,
        ))
        return n

    def html(self):
        t = loader.get_template(self.get_template_display())
        c = json.loads(self.context)

        if self.template == self.TEMPLATE_NEW_COMMENT:
            self.__context_for_new_template(c)

        return t.render(c)

    def __context_for_new_template(self, c):
        comment = get_object_or_404(Comment, pk=c['comment_pk'])
        c['comment'] = comment

        review = comment.review
        suggestion = review.revision.suggestion

        if comment.reply_to:
            c['on_what'] = 'comment'
            c['next_url'] = reverse(
                'suggestion',
                kwargs=dict(
                    goal_slug=suggestion.goal.slug,
                    suggestion_slug=suggestion.slug
                )
            ) + "#sg-comment-%d" % comment.pk
