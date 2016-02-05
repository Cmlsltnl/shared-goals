import re

from django.conf import settings
from django.db import models

from goal.models import Goal, Member

from image_cropping import ImageRatioField
from image_cropping.templatetags.cropping import cropped_thumbnail

from sorl.thumbnail import ImageField


class Proposal(models.Model):
    goal = models.ForeignKey(Goal)
    avg_rating = models.DecimalField(
        max_digits=2, decimal_places=1, default=0.0)
    owner = models.ForeignKey(Member)
    is_draft = models.BooleanField(default=True)
    image = ImageField(
        upload_to="proposals", blank=True)
    cropping = ImageRatioField('image', '360x200')
    slug = models.SlugField('slug', max_length=60, blank=True, unique=True)

    def __str__(self):
        return self.slug + ("(draft)" if self.is_draft else "")

    def get_current_version(self):
        return self.versions.latest('pub_date')

    def apply_cropping_to_image(self):
        def rel_url(url):
            return re.sub("^%s" % settings.MEDIA_URL, "", url)
        self.image = rel_url(
            cropped_thumbnail(None, self, "cropping"))


class Version(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    pub_date = models.DateTimeField(
        'date published', blank=True, auto_now=True)
    proposal = models.ForeignKey(
        Proposal, blank=True, null=True, related_name="versions")

    def __str__(self):
        return "%s_%d" % (self.proposal.slug, self.pk)


class Review(models.Model):
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    owner = models.ForeignKey(Member)
    version = models.ForeignKey(Version, related_name="reviews")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    description = models.TextField(blank=True)
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return "Review by %s for %s" % (self.owner, self.version)
