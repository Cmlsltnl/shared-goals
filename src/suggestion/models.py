import os
import re
import shutil
import urllib

from django.conf import settings
from django.db import models

from goal.models import Goal, Member

from image_cropping import ImageCropField, ImageRatioField
from image_cropping.templatetags.cropping import cropped_thumbnail


class Suggestion(models.Model):
    TYPE_ACTION = 0
    TYPE_PRACTICE = 1

    TYPE_CHOICES = (
        (TYPE_ACTION, 'action'),
        (TYPE_PRACTICE, 'practice'),
    )

    goal = models.ForeignKey(Goal, related_name="suggestions")
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=0)
    avg_rating = models.DecimalField(
        max_digits=2, decimal_places=1, default=0.0)
    owner = models.ForeignKey(Member)
    is_draft = models.BooleanField(default=True)
    image = ImageCropField(upload_to="suggestions", blank=True)
    cropping = ImageRatioField('image', '360x200')
    slug = models.SlugField('slug', max_length=60)
    pub_date = models.DateTimeField('date published', auto_now=True)

    def __str__(self):
        return self.slug + ("(draft)" if self.is_draft else "")

    def get_current_revision(self):
        return self.revisions.latest('pub_date')

    def apply_cropping_to_image(self, delete_original=False):
        if not self.image.name:
            return

        def rel_url(url):
            return re.sub("^%s" % settings.MEDIA_URL, "", url)

        tmp_image_url = rel_url(cropped_thumbnail(None, self, "cropping"))
        rel_tmp_path = urllib.parse.unquote(tmp_image_url)

        rel_cropped_image_path = os.path.join(
            self.image.field.upload_to,
            "suggestion-%d%s" % (self.pk, os.path.splitext(self.image.name)[1])
        )

        if delete_original:
            os.unlink(os.path.join(settings.MEDIA_ROOT, self.image.file.name))
        self.image = rel_cropped_image_path

        shutil.move(
            os.path.join(settings.MEDIA_ROOT, rel_tmp_path),
            os.path.join(settings.MEDIA_ROOT, rel_cropped_image_path)
        )


class Revision(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now=True)
    suggestion = models.ForeignKey(Suggestion, related_name="revisions")

    def __str__(self):
        return "%s_%d" % (self.suggestion.slug, self.pk)
