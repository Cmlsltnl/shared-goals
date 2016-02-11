from django.contrib import admin
from image_cropping import ImageCroppingMixin

from .models import Suggestion, Revision


def apply_cropping_to_image(modeladmin, request, queryset):
    for item in queryset:
        item.apply_cropping_to_image(replace_original=True)
apply_cropping_to_image.short_description = "Apply cropping to image"


class ModelWithImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    actions = [apply_cropping_to_image]


class RevisionAdmin(admin.ModelAdmin):
    list_filter = ('suggestion',)


admin.site.register(Suggestion, ModelWithImageAdmin)
admin.site.register(Revision, RevisionAdmin)
