from django.contrib import admin
from .models import Category, Company, Product

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'company', 'description', 'category', 'owned_by', 'created_at']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Product, ProductAdmin)