"""Models for reviews."""

from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models

from goal.models import GlobalUser

from suggestion.models import Revision


class Review(models.Model):  # noqa
    EXPERIENCE_NOT_TRIED = 0
    EXPERIENCE_TRIED = 1
    EXPERIENCE_DOING = 2

    EXPERIENCE_CHOICES = (
        (EXPERIENCE_NOT_TRIED, "I've not tried this"),
        (EXPERIENCE_TRIED, "Yes, I've tried this myself"),
        (EXPERIENCE_DOING, "I've tried this, and I'm still doing it"),
    )

    pub_date = models.DateTimeField('date published', auto_now=True)
    owner = models.ForeignKey(GlobalUser)
    revision = models.ForeignKey(Revision, related_name="revisions", null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    description = models.TextField(blank=True)
    is_draft = models.BooleanField(default=True)
    experience = models.PositiveSmallIntegerField(
        choices=EXPERIENCE_CHOICES, default=0, blank=True)

    def __str__(self):  # noqa
        return "Review by %s for %s" % (self.owner, self.revision)

    @property
    def header(self):  # noqa
        header = self.owner.name
        header += ", %s" % naturaltime(self.pub_date)
        return header

    def published_comments(self):  # noqa
        comments = [
            c for c in self.comments.filter(
                is_draft=False, reply_to=None
            ).order_by("pub_date")
        ]

        result = []
        while len(comments):
            comment = comments.pop()
            result.append(comment)
            for reply in (
                comment.replies.filter(is_draft=False).order_by("pub_date")
            ):
                comments.append(reply)

        return result


class Comment(models.Model):  # noqa
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    owner = models.ForeignKey(GlobalUser)

    review = models.ForeignKey(Review, related_name="comments")
    reply_to = models.ForeignKey(
        'self', blank=True, null=True, related_name="replies")

    body = models.TextField()
    is_draft = models.BooleanField(default=True)

    def __str__(self):  # noqa
        return (
            "Comment by %s on %s (%s)"
            % (self.owner, self.review, self.reply_to_id)
        )

    def indent(self):  # noqa
        result = 0
        current = self
        while current.reply_to:
            result += 20
            current = current.reply_to
        return result
