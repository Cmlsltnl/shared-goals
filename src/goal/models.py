from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class GlobalUser(models.Model):
    user = models.OneToOneField(User)
    join_date = models.DateTimeField('date joined', auto_now_add=True)
    image = models.FileField(blank=True, upload_to='members')

    @property
    def name(self):
        return self.user.username

    def __str__(self):
        return self.name


class Goal(models.Model):
    title = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    slug = models.SlugField('slug', max_length=60, unique=True)
    image = models.FileField(blank=True, upload_to='goals')
    owner = models.ForeignKey(GlobalUser)
    is_draft = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Goal, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Member(models.Model):
    global_user = models.ForeignKey(GlobalUser, related_name="memberships")
    goal = models.ForeignKey(Goal, related_name="members")
    join_date = models.DateTimeField('date joined', auto_now_add=True)
    image = models.FileField(blank=True, upload_to='members')

    @property
    def name(self):
        return self.global_user.name

    def __str__(self):
        return self.name
