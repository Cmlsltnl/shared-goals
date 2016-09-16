"""Utility functions."""

import os
from PIL import Image
from django.conf import settings


def apply_cropping_to_image(image, x, y, w, h, output_filename=None):
    """Replace image with a cropped iamge."""
    if not image.name:
        return

    img_filename = os.path.join(settings.MEDIA_ROOT, image.name)
    img = Image.open(img_filename)
    img = img.crop((int(x), int(y), int(x + w), int(y + h)))
    img.save(output_filename or img_filename)


def singlify(queryDict):  # noqa
    """Convert queryDict into a normal dict.

    Return a dict of queryDict where lists of size 1 are replaced
    with a single value.
    """
    result = {}
    for key in queryDict:
        val = queryDict.get(key)
        if isinstance(val, type([])) and len(val) == 1:
            val = val[0]
        result[key] = val
    return result
