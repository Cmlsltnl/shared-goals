import os
import re
import shutil
import urllib

from django.conf import settings
from django.db import models

from goal.models import Goal, Member

from image_cropping import ImageCropField, ImageRatioField
from image_cropping.templatetags.cropping import cropped_thumbnail


class Proposal(models.Model):
    goal = models.ForeignKey(Goal, related_name="proposals")
    avg_rating = models.DecimalField(
        max_digits=2, decimal_places=1, default=0.0)
    owner = models.ForeignKey(Member)
    is_draft = models.BooleanField(default=True)
    image = ImageCropField(upload_to="proposals", blank=True)
    cropping = ImageRatioField('image', '360x200')
    slug = models.SlugField('slug', max_length=60)
    pub_date = models.DateTimeField('date published', auto_now=True)

    def __str__(self):
        return self.slug + ("(draft)" if self.is_draft else "")

    def get_current_revision(self):
        return self.revisions.latest('pub_date')

    def apply_cropping_to_image(self, replace_original=False):
        if not self.image.name:
            return

        def rel_url(url):
            return re.sub("^%s" % settings.MEDIA_URL, "", url)

        new_image_url = rel_url(cropped_thumbnail(None, self, "cropping"))
        new_image_path = urllib.parse.unquote(new_image_url)
        if replace_original:
            shutil.move(
                os.path.join(settings.MEDIA_ROOT, new_image_path),
                self.image.file.name
            )
        else:
            self.image = new_image_path


class Revision(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now=True)
    proposal = models.ForeignKey(Proposal, related_name="revisions")

    def __str__(self):
        return "%s_%d" % (self.proposal.slug, self.pk)
