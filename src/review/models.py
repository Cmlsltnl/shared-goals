from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models

from goal.models import GlobalUser, Member

from suggestion.models import Revision


class Review(models.Model):
    EXPERIENCE_NOT_TRIED = 0
    EXPERIENCE_DID_NOT_WORK = 1
    EXPERIENCE_WORKED_IN_PAST = 2
    EXPERIENCE_WORKS_NOW = 3

    EXPERIENCE_CHOICES = (
        (EXPERIENCE_NOT_TRIED, "I've not (really) tried this"),
        (EXPERIENCE_DID_NOT_WORK, "I've tried this but it didn't work for me"),
        (EXPERIENCE_WORKED_IN_PAST, "This has worked for me in the past"),
        (EXPERIENCE_WORKS_NOW, "This is working for me now"),
    )

    pub_date = models.DateTimeField('date published', auto_now=True)
    owner = models.ForeignKey(Member)
    revision = models.ForeignKey(Revision, related_name="revisions", null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    description = models.TextField(blank=True)
    is_draft = models.BooleanField(default=True)
    experience = models.PositiveSmallIntegerField(
        choices=EXPERIENCE_CHOICES, default=0, blank=True)

    def __str__(self):
        return "Review by %s for %s" % (self.owner, self.revision)

    @property
    def header(self):
        header = \
            "Reviewed by " if self.description \
            else "Rated by "
        header += self.owner.global_user.name
        header += ", %s" % naturaltime(self.pub_date)
        return header

    def published_comments(self):
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


class Comment(models.Model):
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    owner = models.ForeignKey(GlobalUser)

    review = models.ForeignKey(Review, related_name="comments")
    reply_to = models.ForeignKey(
        'self', blank=True, null=True, related_name="replies")

    body = models.TextField()
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return "Comment by %s on %s" % (self.owner, self.target)

    def indent(self):
        result = 0
        current = self
        while current.reply_to:
            result += 20
            current = current.reply_to
        return result
