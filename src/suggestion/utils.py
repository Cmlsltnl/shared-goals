import os
import re
import shutil
import urllib

from django.conf import settings

from image_cropping.templatetags.cropping import cropped_thumbnail


def apply_cropping_to_image(suggestion, delete_original=False):
    if not suggestion.image.name:
        return

    def rel_url(url):
        return re.sub("^%s" % settings.MEDIA_URL, "", url)

    tmp_image_url = rel_url(cropped_thumbnail(None, suggestion, "cropping"))
    rel_tmp_path = urllib.parse.unquote(tmp_image_url)

    rel_cropped_image_path = os.path.join(
        suggestion.image.field.upload_to,
        "suggestion-%d%s" % (
            suggestion.pk, os.path.splitext(suggestion.image.name)[1])
    )

    if delete_original:
        os.unlink(
            os.path.join(settings.MEDIA_ROOT, suggestion.image.file.name))
    suggestion.image = rel_cropped_image_path

    shutil.move(
        os.path.join(settings.MEDIA_ROOT, rel_tmp_path),
        os.path.join(settings.MEDIA_ROOT, rel_cropped_image_path)
    )
