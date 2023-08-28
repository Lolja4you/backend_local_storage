from django.contrib import admin

from .models import *

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    pass

@admin.register(MultipleAlbum)
class MediaAdmin(admin.ModelAdmin):
    pass