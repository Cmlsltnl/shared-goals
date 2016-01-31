from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Goal(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    slug = models.SlugField('slug', max_length=60, blank=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Goal, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Member(models.Model):
    user = models.ForeignKey(User)
    join_date = models.DateTimeField('date joined')

    def __str__(self):
        return self.user.get_full_name()
