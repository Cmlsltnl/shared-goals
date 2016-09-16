"""Suggestion models."""

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify


class GlobalUser(models.Model):
    """Any user of Shared Goals."""

    user = models.OneToOneField(User, related_name="global_user")
    join_date = models.DateTimeField('date joined', auto_now_add=True)
    image = models.FileField(blank=True, upload_to='members')

    @property
    def name(self):  # noqa
        return self.user.username

    def __str__(self):  # noqa
        return self.name


class Goal(models.Model):  # noqa
    title = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    slug = models.SlugField('slug', max_length=60, unique=True)
    image = models.FileField(blank=True, upload_to='goals')
    owner = models.ForeignKey(GlobalUser)
    is_draft = models.BooleanField(default=True)

    def save(self, *args, **kwargs):  # noqa
        if not self.id:
            self.slug = slugify(self.title)
        super(Goal, self).save(*args, **kwargs)

    def get_url(self):  # noqa
        return reverse(
            'goal',
            kwargs=dict(goal_slug=self.slug)
        )

    def __str__(self):  # noqa
        return self.title


class Member(models.Model):
    """Member of a Goal."""

    global_user = models.ForeignKey(GlobalUser, related_name="memberships")
    goal = models.ForeignKey(Goal, related_name="members")
    join_date = models.DateTimeField('date joined', auto_now_add=True)
    image = models.FileField(blank=True, upload_to='members')

    @property
    def name(self):  # noqa
        return self.global_user.name

    @staticmethod
    def lookup(user, goal_slug):
        """Look up a member given a user and goal_slug."""
        try:
            return Member.objects.get(
                global_user__user=user,
                goal__slug=goal_slug
            )
        except Member.DoesNotExist:
            return None

    def __str__(self):  # noqa
        return self.name
