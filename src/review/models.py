from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import models

from goal.models import GlobalUser, Member

from proposal.models import Revision


class Comment(models.Model):
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    owner = models.ForeignKey(GlobalUser)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey('content_type', 'object_id')

    body = models.TextField()
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return "Comment by %s on %s" % (self.owner, self.target)


class Review(models.Model):
    pub_date = models.DateTimeField('date published', auto_now=True)
    owner = models.ForeignKey(Member)
    revision = models.ForeignKey(Revision, related_name="revisions", null=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    description = models.TextField(blank=True)
    is_draft = models.BooleanField(default=True)
    comments = GenericRelation(Comment)

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
        return self.comments.filter(is_draft=False)
