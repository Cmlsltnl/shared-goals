import os
from PIL import Image
from django.conf import settings


def apply_cropping_to_image(image, x, y, w, h, output_filename=None):
    if not image.name:
        return

    img_filename = os.path.join(settings.MEDIA_ROOT, image.name)
    img = Image.open(img_filename)
    img = img.crop((int(x), int(y), int(x + w), int(y + h)))
    img.save(output_filename or img_filename)
