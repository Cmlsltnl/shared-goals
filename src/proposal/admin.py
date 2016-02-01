from django.contrib import admin

# Register your models here.
from .models import Proposal, Rating

admin.site.register(Proposal)
admin.site.register(Rating)
