from django.db import models
from goal.models import Goal, Member
from django.template.defaultfilters import slugify


class Proposal(models.Model):
    title = models.CharField(max_length=100, unique=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    goal = models.ForeignKey(Goal)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    owner = models.ForeignKey(Member)
    image_url = models.URLField(blank=True)
    slug = models.SlugField('slug', max_length=60, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Proposal, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
