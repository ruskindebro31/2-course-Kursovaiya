from django.contrib import admin

from .models.review import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'candle', 'rating', 'created_at')
    list_display_links = ('id',)
    list_filter = ('rating', 'created_at')
    search_fields = ('user__username', 'user__email', 'candle__name', 'comment')
    readonly_fields = ('created_at',)
    list_per_page = 25
