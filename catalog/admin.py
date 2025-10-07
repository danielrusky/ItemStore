from django.contrib import admin

from catalog.models import Product, Category, Contacts, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category',)
    list_filter = ('category',)
    search_fields = ('name', 'description',)


admin.site.register(Contacts)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "v_number", "v_name", "current", "add_date")
    list_filter = ("v_name", "v_number", "current", "add_date")
    search_fields = ("product",)
