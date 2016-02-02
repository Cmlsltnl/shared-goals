from django.contrib import admin

# Register your models here.
from .models import Proposal, Review

admin.site.register(Proposal)
admin.site.register(Review)
