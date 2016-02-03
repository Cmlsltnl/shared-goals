from django.contrib import admin
from image_cropping import ImageCroppingMixin
from .models import Goal, Member


class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    pass


admin.site.register(Goal, MyModelAdmin)
admin.site.register(Member, MyModelAdmin)
