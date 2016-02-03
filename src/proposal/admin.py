from django.contrib import admin

# Register your models here.
from .models import Proposal, ProposalVersion, Review

admin.site.register(Proposal)
admin.site.register(ProposalVersion)
admin.site.register(Review)
