from django.contrib import admin

from .models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'candle', 'created_at')
    list_display_links = ('id',)
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'candle__name')
    readonly_fields = ('created_at',)
