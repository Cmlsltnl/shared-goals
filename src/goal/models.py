from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from image_cropping import ImageRatioField

from sorl.thumbnail import ImageField as SorlImageField


class Goal(models.Model):
    title = models.CharField(max_length=100, unique=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    slug = models.SlugField('slug', max_length=60, blank=True, unique=True)
    image = models.ImageField(blank=True, upload_to='goals')
    cropping = ImageRatioField('image', '430x360')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Goal, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Member(models.Model):
    user = models.ForeignKey(User)
    join_date = models.DateTimeField('date joined')
    image = SorlImageField(blank=True, upload_to='members')
    cropping = ImageRatioField('image', '360x430')

    def __str__(self):
        return self.user.username
