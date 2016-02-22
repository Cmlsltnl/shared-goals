from django.contrib import admin

from .models import Suggestion, Revision

from review.utils import update_rating_and_save


def update_avg_rating(modeladmin, request, queryset):
    for suggestion in queryset:
        update_rating_and_save(suggestion)
update_avg_rating.short_description = "Update average rating"


class SuggestionAdmin(admin.ModelAdmin):
    actions = [update_avg_rating]


class RevisionAdmin(admin.ModelAdmin):
    list_filter = ('suggestion',)


admin.site.register(Suggestion, SuggestionAdmin)
admin.site.register(Revision, RevisionAdmin)
