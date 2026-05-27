from django.contrib import admin
from django.utils.html import format_html

from apps.catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "image_thumbnail", "category", "price", "stock", "is_active", "created_at")
    list_filter = ("category", "is_active")
    list_editable = ("price", "stock", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "image_preview")
    fieldsets = (
        (None, {"fields": ("category", "name", "slug", "description", "price", "stock", "is_active")}),
        (
            "Изображение",
            {
                "fields": ("image", "image_preview"),
                "description": "Файл сохраняется в каталоге media/products/ относительно MEDIA_ROOT (см. настройки проекта).",
            },
        ),
        ("Служебное", {"fields": ("created_at",)}),
    )

    @admin.display(description="Превью в списке")
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="44" height="44" style="object-fit:cover;border-radius:6px" alt="" />',
                obj.image.url,
            )
        return "—"

    @admin.display(description="Превью")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:240px;max-height:240px;border-radius:10px;object-fit:contain" alt="" />',
                obj.image.url,
            )
        return "Загрузите файл выше — после сохранения здесь появится миниатюра."
