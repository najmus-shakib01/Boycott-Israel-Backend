import os
from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display
from .models import BlobPhoto, BlobVideo
from boycottIsrael.supabase_storage import upload_to_supabase

class BlobPhotoAdminForm(forms.ModelForm):
    upload_file = forms.FileField(
        required=False,
        label="ছবি ফাইল নির্বাচন করুন (সুপাবেসে আপলোড হবে)",
        help_text="কম্পিউটার থেকে ছবি নির্বাচন করুন। সর্বোচ্চ সাইজ: ৫ মেগাবাইট (JPG, PNG, WebP, AVIF)"
    )
    photo = forms.CharField(
        required=False,
        label="অথবা ছবির সরাসরি URL পেস্ট করুন",
        help_text="ফাইল নির্বাচন না করলে এখানে সরাসরি কোনো ইমেজ লিংক পেস্ট করতে পারেন।"
    )

    class Meta:
        model = BlobPhoto
        fields = ['photoTitle', 'upload_file', 'photo']

    def clean(self):
        cleaned_data = super().clean()
        upload_file = cleaned_data.get('upload_file')
        photo_url = cleaned_data.get('photo')

        if not upload_file and not photo_url:
            raise ValidationError("অনুগ্রহ করে একটি ছবি ফাইল নির্বাচন করুন অথবা একটি ছবির URL দিন।")

        if upload_file:
            # সর্বোচ্চ সাইজ ভ্যালিডেশন (5 MB)
            max_size = 5 * 1024 * 1024
            if upload_file.size > max_size:
                size_mb = upload_file.size / (1024 * 1024)
                raise ValidationError(f"ফাইলের সাইজ ৫ মেগাবাইট (5 MB)-এর বেশি হতে পারবে না! আপনার ফাইলের সাইজ: {size_mb:.2f} MB")

            ext = os.path.splitext(upload_file.name)[1].lower()
            allowed = ['.jpg', '.jpeg', '.png', '.webp', '.avif', '.gif']
            if ext not in allowed:
                raise ValidationError(f"ভুল ফরম্যাট! শুধুমাত্র {', '.join(allowed)} ফরম্যাটের ছবি গ্রহণযোগ্য।")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        upload_file = self.cleaned_data.get('upload_file')
        if upload_file:
            public_url = upload_to_supabase(upload_file, folder="photos")
            instance.photo = public_url
        if commit:
            instance.save()
        return instance

class BlobVideoAdminForm(forms.ModelForm):
    upload_file = forms.FileField(
        required=False,
        label="ভিডিও ফাইল নির্বাচন করুন (সুপাবেসে আপলোড হবে)",
        help_text="কম্পিউটার থেকে ভিডিও নির্বাচন করুন। সর্বোচ্চ সাইজ: ৫০ মেগাবাইট (MP4, WebM, MOV)"
    )
    video = forms.CharField(
        required=False,
        label="অথবা ভিডিওর সরাসরি URL পেস্ট করুন",
        help_text="ফাইল নির্বাচন না করলে এখানে সরাসরি কোনো ভিডিওর URL পেস্ট করতে পারেন।"
    )

    class Meta:
        model = BlobVideo
        fields = ['videoTitle', 'upload_file', 'video']

    def clean(self):
        cleaned_data = super().clean()
        upload_file = cleaned_data.get('upload_file')
        video_url = cleaned_data.get('video')

        if not upload_file and not video_url:
            raise ValidationError("অনুগ্রহ করে একটি ভিডিও ফাইল নির্বাচন করুন অথবা একটি ভিডিওর URL দিন।")

        if upload_file:
            # সর্বোচ্চ সাইজ ভ্যালিডেশন (50 MB)
            max_size = 50 * 1024 * 1024
            if upload_file.size > max_size:
                size_mb = upload_file.size / (1024 * 1024)
                raise ValidationError(f"ভিডিও ফাইলের সাইজ ৫০ মেগাবাইট (50 MB)-এর বেশি হতে পারবে না! আপনার ফাইলের সাইজ: {size_mb:.2f} MB")

            ext = os.path.splitext(upload_file.name)[1].lower()
            allowed = ['.mp4', '.webm', '.mov', '.mkv']
            if ext not in allowed:
                raise ValidationError(f"ভুল ফরম্যাট! শুধুমাত্র {', '.join(allowed)} ফরম্যাটের ভিডিও গ্রহণযোগ্য।")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        upload_file = self.cleaned_data.get('upload_file')
        if upload_file:
            public_url = upload_to_supabase(upload_file, folder="videos")
            instance.video = public_url
        if commit:
            instance.save()
        return instance

@admin.register(BlobPhoto)
class BlobPhotoAdmin(ModelAdmin):
    form = BlobPhotoAdminForm
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
    form = BlobVideoAdminForm
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
