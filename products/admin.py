import os
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.decorators import display
from .models import Category, Company, Product
from boycottIsrael.supabase_storage import upload_to_supabase

# Style default Django Auth with Unfold
admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

class ProductInline(TabularInline):
    model = Product
    extra = 0
    fields = ['category', 'owned_by', 'description']
    show_change_link = True

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'products_count']
    search_fields = ['name']
    list_filter_submit = True

    @display(description="মোট পণ্য", label=True)
    def products_count(self, obj):
        return f"{obj.products.count()} টি"

class CompanyAdminForm(forms.ModelForm):
    upload_file = forms.FileField(
        required=False,
        label="লোগো ফাইল নির্বাচন করুন (সুপাবেসে আপলোড হবে)",
        help_text="কম্পিউটার থেকে লোগো নির্বাচন করুন। সর্বোচ্চ সাইজ: ২ মেগাবাইট (PNG, JPG, WebP, SVG)"
    )
    logo = forms.CharField(
        required=False,
        label="অথবা লোগোর সরাসরি URL পেস্ট করুন",
        help_text="ফাইল নির্বাচন না করলে এখানে সরাসরি কোনো লোগো লিংক পেস্ট করতে পারেন।"
    )

    class Meta:
        model = Company
        fields = ['name', 'upload_file', 'logo']

    def clean(self):
        cleaned_data = super().clean()
        upload_file = cleaned_data.get('upload_file')
        logo_url = cleaned_data.get('logo')

        if not upload_file and not logo_url:
            raise ValidationError("অনুগ্রহ করে একটি লোগো ফাইল নির্বাচন করুন অথবা একটি লোগোর URL দিন।")

        if upload_file:
            max_size = 2 * 1024 * 1024
            if upload_file.size > max_size:
                size_mb = upload_file.size / (1024 * 1024)
                raise ValidationError(f"লোগো ফাইলের সাইজ ২ মেগাবাইট (2 MB)-এর বেশি হতে পারবে না! আপনার ফাইলের সাইজ: {size_mb:.2f} MB")

            ext = os.path.splitext(upload_file.name)[1].lower()
            allowed = ['.png', '.jpg', '.jpeg', '.webp', '.svg']
            if ext not in allowed:
                raise ValidationError(f"ভুল ফরম্যাট! শুধুমাত্র {', '.join(allowed)} ফরম্যাটের লোগো গ্রহণযোগ্য।")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        upload_file = self.cleaned_data.get('upload_file')
        if upload_file:
            public_url = upload_to_supabase(upload_file, folder="products")
            instance.logo = public_url
        if commit:
            instance.save()
        return instance

@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    form = CompanyAdminForm
    list_display = ['logo_preview', 'name', 'total_products', 'logo_link']
    search_fields = ['name']
    list_filter_submit = True
    inlines = [ProductInline]

    @display(description="লোগো")
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height: 38px; width: 38px; object-fit: contain; '
                'border-radius: 8px; background: #ffffff; padding: 2px; '
                'border: 1px solid #e2e8f0; box-shadow: 0 1px 2px rgba(0,0,0,0.05);" />',
                obj.logo
            )
        return format_html('<span style="color: #94a3b8; font-size: 12px;">লোগো নেই</span>')

    @display(description="পণ্য সংখ্যা", label=True)
    def total_products(self, obj):
        return f"{obj.products.count()} টি পণ্য"

    @display(description="স্টোরেজ লিংক")
    def logo_link(self, obj):
        if obj.logo:
            return format_html(
                '<a href="{}" target="_blank" style="color: #10b981; text-decoration: underline; font-size: 12px;">ছবি দেখুন ↗</a>',
                obj.logo
            )
        return "-"

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['company_thumbnail', 'company', 'category', 'owned_by', 'created_at']
    list_filter = ['category', 'company']
    search_fields = ['company__name', 'category__name', 'description', 'owned_by']
    autocomplete_fields = ['company', 'category']
    list_filter_submit = True
    list_per_page = 25

    @display(description="লোগো")
    def company_thumbnail(self, obj):
        if obj.company and obj.company.logo:
            return format_html(
                '<img src="{}" style="height: 32px; width: 32px; object-fit: contain; '
                'border-radius: 6px; background: #ffffff; padding: 2px; border: 1px solid #e2e8f0;" />',
                obj.company.logo
            )
        return "-"
