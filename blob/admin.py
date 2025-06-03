from django.contrib import admin
from .models import BlobPhoto, BlobVideo

class BlobPhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'photoTitle', 'photo', 'created_at']

class BlobVideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'videoTitle', 'video', 'created_at']

admin.site.register(BlobPhoto, BlobPhotoAdmin)
admin.site.register(BlobVideo, BlobVideoAdmin)