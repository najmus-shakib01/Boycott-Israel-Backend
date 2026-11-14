from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.decorators import display
from .models import Category, Company, Product

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

@admin.register(Company)
class CompanyAdmin(ModelAdmin):
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
