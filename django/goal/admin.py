from django.contrib import admin
from .models import GlobalUser, Goal, Member


admin.site.register(GlobalUser)
admin.site.register(Goal)
admin.site.register(Member)
