from django.contrib import admin
from image_cropping import ImageCroppingMixin

from .models import Suggestion, Revision
from .utils import apply_cropping_to_image

from review.utils import update_rating_and_save


def crop_image(modeladmin, request, queryset):
    for item in queryset:
        apply_cropping_to_image(item, delete_original=True)
        item.save()
crop_image.short_description = "Apply cropping to image"


def update_avg_rating(modeladmin, request, queryset):
    for suggestion in queryset:
        update_rating_and_save(suggestion)
update_avg_rating.short_description = "Update average rating"


class ModelWithImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    actions = [crop_image, update_avg_rating]


class RevisionAdmin(admin.ModelAdmin):
    list_filter = ('suggestion',)


admin.site.register(Suggestion, ModelWithImageAdmin)
admin.site.register(Revision, RevisionAdmin)
