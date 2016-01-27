from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from goal.models import Goal


@python_2_unicode_compatible
class Proposal(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    goal = models.ForeignKey(Goal)

    def __str__(self):
        return self.title
