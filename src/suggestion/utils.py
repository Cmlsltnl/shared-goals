import os
import re
import shutil

try:
    from urllib.parse import unquote
except ImportError:
    from urllib import unquote

from django.conf import settings

from image_cropping.templatetags.cropping import cropped_thumbnail


def apply_cropping_to_image(item, delete_original=False):
    if not item.image.name:
        return

    def rel_url(url):
        return re.sub("^%s" % settings.MEDIA_URL, "", url)

    tmp_image_url = rel_url(cropped_thumbnail(None, item, "cropping"))
    rel_tmp_path = unquote(tmp_image_url)

    rel_cropped_image_path = os.path.join(
        item.image.field.upload_to,
        "%s-%d%s" % (
            item.image.field.upload_to,
            item.pk,
            os.path.splitext(item.image.name)[1]
        )
    )

    if delete_original:
        os.unlink(
            os.path.join(settings.MEDIA_ROOT, item.image.file.name))
    item.image = rel_cropped_image_path

    shutil.move(
        os.path.join(settings.MEDIA_ROOT, rel_tmp_path),
        os.path.join(settings.MEDIA_ROOT, rel_cropped_image_path)
    )
