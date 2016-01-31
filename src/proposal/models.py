from django.db import models
from goal.models import Goal, Member


class Proposal(models.Model):
    title = models.CharField(max_length=200, unique=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    goal = models.ForeignKey(Goal)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    owner = models.ForeignKey(Member)
    image_url = models.URLField()

    def __str__(self):
        return self.title
