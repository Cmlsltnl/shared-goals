from django.contrib import admin
from image_cropping import ImageCroppingMixin

# Register your models here.
from .models import Comment, Proposal, Revision, Review


def apply_cropping_to_image(modeladmin, request, queryset):
    for item in queryset:
        item.apply_cropping_to_image(replace_original=True)
apply_cropping_to_image.short_description = "Apply cropping to image"


class ModelWithImageAdmin(ImageCroppingMixin, admin.ModelAdmin):
    actions = [apply_cropping_to_image]


class RevisionAdmin(admin.ModelAdmin):
    list_filter = ('proposal',)


admin.site.register(Comment)
admin.site.register(Proposal, ModelWithImageAdmin)
admin.site.register(Review)
admin.site.register(Revision, RevisionAdmin)
