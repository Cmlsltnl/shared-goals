from django.db import models


class Goal(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
