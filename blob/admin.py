from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import BlobPhoto, BlobVideo

@admin.register(BlobPhoto)
class BlobPhotoAdmin(ModelAdmin):
    list_display = ['photo_thumbnail', 'photo_title_short', 'photo_link', 'created_at']
    search_fields = ['photoTitle']
    list_filter_submit = True
    list_per_page = 20

    @display(description="ছবি প্রিভিউ")
    def photo_thumbnail(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="height: 48px; width: 68px; object-fit: cover; '
                'border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 2px rgba(0,0,0,0.08);" />',
                obj.photo
            )
        return format_html('<span style="color: #94a3b8;">ছবি নেই</span>')

    @display(description="শিরোনাম")
    def photo_title_short(self, obj):
        if len(obj.photoTitle) > 60:
            return f"{obj.photoTitle[:60]}..."
        return obj.photoTitle

    @display(description="সুপাবেস লিংক")
    def photo_link(self, obj):
        if obj.photo:
            return format_html(
                '<a href="{}" target="_blank" style="color: #10b981; font-weight: 500; text-decoration: underline;">ওপেন করুন ↗</a>',
                obj.photo
            )
        return "-"

@admin.register(BlobVideo)
class BlobVideoAdmin(ModelAdmin):
    list_display = ['video_title_short', 'video_link', 'created_at']
    search_fields = ['videoTitle']
    list_filter_submit = True
    list_per_page = 20

    @display(description="ভিডিওর শিরোনাম")
    def video_title_short(self, obj):
        if len(obj.videoTitle) > 60:
            return f"{obj.videoTitle[:60]}..."
        return obj.videoTitle

    @display(description="ভিডিও প্লে করুন")
    def video_link(self, obj):
        if obj.video:
            return format_html(
                '<a href="{}" target="_blank" style="display: inline-flex; align-items: center; gap: 4px; '
                'background: #10b981; color: #ffffff; padding: 4px 10px; border-radius: 6px; '
                'text-decoration: none; font-size: 12px; font-weight: 500;">'
                '▶ ভিডিও দেখুন'
                '</a>',
                obj.video
            )
        return "-"
