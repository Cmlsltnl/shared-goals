from django.db import models
from django.contrib.auth.models import User


class Goal(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title


class Member(models.Model):
    user = models.ForeignKey(User)
    join_date = models.DateTimeField('date joined')

    def __str__(self):
        return self.user.get_full_name()
