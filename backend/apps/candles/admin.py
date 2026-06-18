from django.contrib import admin

from .models import Category, Candle


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'is_active')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'slug', 'description')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Candle)
class CandleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'category', 'season', 'price', 'is_published', 'author', 'created_at',
    )
    list_display_links = ('id', 'name')
    list_filter = ('category', 'season', 'is_published', 'created_at')
    search_fields = ('name', 'description')
    list_editable = ('is_published', 'price')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25
    date_hierarchy = 'created_at'
    fieldsets = (
        (None, {'fields': ('name', 'description', 'price', 'category', 'season', 'image')}),
        ('Публикация', {'fields': ('is_published', 'author')}),
        ('Даты', {'fields': ('created_at', 'updated_at')}),
    )
