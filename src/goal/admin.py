from django.contrib import admin

# Register your models here.
from .models import Goal, Member

admin.site.register(Goal)
admin.site.register(Member)
