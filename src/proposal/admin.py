from django.contrib import admin
from image_cropping import ImageCroppingMixin

# Register your models here.
from .models import Proposal, Version, Review


class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


admin.site.register(Proposal, MyModelAdmin)
admin.site.register(Version, MyModelAdmin)
admin.site.register(Review, MyModelAdmin)
