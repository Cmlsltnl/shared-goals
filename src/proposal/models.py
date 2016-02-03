from django.db import models
from goal.models import Goal, Member
from sorl.thumbnail import ImageField
from image_cropping import ImageRatioField


class Proposal(models.Model):
    goal = models.ForeignKey(Goal)
    avg_rating = models.DecimalField(
        max_digits=2, decimal_places=1, default=0.0)
    owner = models.ForeignKey(Member)
    current_version = models.ForeignKey('ProposalVersion', related_name="+")
    is_draft = models.BooleanField(default=True)
    image = ImageField(
        upload_to="proposals", blank=True)
    cropping = ImageRatioField('image', '430x360')
    slug = models.SlugField('slug', max_length=60, blank=True, unique=True)

    def __str__(self):
        return self.title


class ProposalVersion(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    pub_date = models.DateTimeField(
        'date published', blank=True, auto_now=True)
    proposal = models.ForeignKey(Proposal, blank=True, null=True)


class Review(models.Model):
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    owner = models.ForeignKey(Member)
    proposal_version = models.ForeignKey(ProposalVersion)
    rating = models.PositiveSmallIntegerField(default=0)
    description = models.TextField()

    def __str__(self):
        return "Review for %s" % self.proposal.title
